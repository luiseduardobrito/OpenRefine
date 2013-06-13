import urllib, sys, os, glob, zipfile
from xml.dom import minidom

class Launcher:

	_remote  = "https://gist.github.com/luiseduardobrito/5750844/raw/3216b5c8243aae0c717bc7d4826836a66ae3dbe3/config.xml"
	_local   = "config.xml"

	_remote_workspace = "https://github.com/luiseduardobrito/OpenRefine/blob/gpnx/workspace.zip?raw=true"
	_local_workspace  = "projects/workspace.zip"

	_path    = "projects/"
	_version = "0.1"

	def unzip(self, zipFilePath, destDir):
	    zfile = zipfile.ZipFile(zipFilePath)
	    for name in zfile.namelist():
	        (dirName, fileName) = os.path.split(name)
	        if fileName == '':
	            # directory
	            newDir = destDir + '/' + dirName
	            if not os.path.exists(newDir):
	                os.mkdir(newDir)
	        else:
	            # file
	            fd = open(destDir + '/' + name, 'wb')
	            fd.write(zfile.read(name))
	            fd.close()
	    zfile.close()

	def getText(self, nodelist):
	    rc = []
	    for node in nodelist:
	        if node.nodeType == node.TEXT_NODE:
	            rc.append(node.data)
	    return ''.join(rc)

	def handleTok(self, tokenlist):
	    texts = ""
	    for token in tokenlist:
	        texts += " "+ self.getText(token.childNodes)
	    return texts

	def _log(self, msg):
		print msg

	def check_updates(self, config_url = ''):
		self._log("Getting update information from server...")
		remote_version = self.get_remote_version(self._remote)

		self._log("Remote version: %s" % remote_version)

		if(self._version == remote_version):
			self._log("Client already in latest version.")
			return
		else:
			self.update_projects()

	def update_projects(self):
		self._log("Downloading projects metadata...")
		urllib.urlretrieve (self._remote_workspace, self._local_workspace)

		self._log("Inflating projects files...")
		self.unzip(self._local_workspace, self._path)

		self._log("Added projects to OpenRefine workspace successfully...")

	def purge(self):
		self._log("Purging configuration files...")
		os.remove(self._local)

		self._log("Download untouched configuration file from server...")
		urllib.urlretrieve (self._remote, self._local)

		self._log("Deleting all projects...")
		os.rmdir(self._projects)

		self._log("Downloading projects files. Please, be a little patient, it may take some time...")
		urllib.urlretrieve (self._remote_workspace, self._local_workspace)

		self._log("Configurations purged successfully")

	def get_remote_version(self, input):
		xmldoc = minidom.parse(urllib.urlopen(input))
		config = xmldoc.getElementsByTagName("config")[0]
		return self.handleTok(config.getElementsByTagName("version"))

	def get_local_version(self):
		xmldoc = minidom.parse(open(self._local, "r"))
		config = xmldoc.getElementsByTagName("config")[0]

		if(config):
			return self.handleTok(config.getElementsByTagName("version"))
		else:
			self._log("No configuration information found, downloading new one...");
			self.purge()
			check_updates()

	def _info(self):
		self._log("\nGPNX Refine - Customized large data manipulated solution")
		self._log("Copyright 2013 - GPNX Group")
		self._log("Redesigned by Luis Eduardo Brito <luis@gpnxgroup.com>\n")
		return

	def _help(self):
		self._info()
		self._howto()
		self._log("")
		return

	def _howto(self):
		self._log("How to:")
		self._log("    python refine.py [options]\n")
		self._log("Available options:")
		self._log("    --version               get local version")
		self._log("    --skip-update-check     skip remote check, just take me to the grefine")
		self._log("    --purge-installation    purge all stuff and redownload from remote")
		self._log("    --help                  SOS: help me")
		return

	def version(self):
		self._info()
		self._log("Local version: %s" % self.get_local_version())
		self._log("")
		return

	def run(self):
		self._log("Starting OpenRefine jetty server...")
		os.system('./launcher -d %s'%self._path)
		return

	def __init__(self):

		# --help
		if(len(sys.argv) > 1 and (sys.argv[1] == "--help" or sys.argv[1] == "-h" or sys.argv[1] == "help")):
			self._help()
			return

		# --versiom
		if(len(sys.argv) > 1 and (sys.argv[1] == "--version" or sys.argv[1] == "-v" or sys.argv[1] == "version")):
			self.version()
			return

		# --purge-installation
		if(len(sys.argv) > 1 and (sys.argv[1] == "--purge-installation" or sys.argv[1] == "-p" or sys.argv[1] == "purge")):
			self.purge()
			return

		self._log("GPNX Refine - Initializing launcher resources...")

		if(len(sys.argv) > 1 and sys.argv[1] == "--skip-update-check"):
			self.run()
			return

		self.check_updates()
		self.run()

l = Launcher()