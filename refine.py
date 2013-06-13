import sys, os, zipfile, shutil, urllib.request
from urllib.request import urlopen
from urllib.request import urlretrieve
from xml.dom import minidom

class Launcher:

	_path    = "workspace/"
	_version = "0.1"

	_remote  = "https://gist.github.com/luiseduardobrito/5750844/raw/49d8ad6266739ad0deefeaecfca7023af0b1dac0/config.xml"
	_local   = "config.xml"

	_local_workspace  = _path + "workspace.zip"
	_main_workspace = "main"

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
		print(msg)

	def check_updates(self, config_url = ''):
		self._log("Getting update information from server...")
		self._version = self.get_local_version()
		(v, w) = self.get_remote_info(self._remote)

		self._log("Local workspace version: %s" % self._version)

		if(self._version == v):
			self._log("Client already in latest version.")
			return
		else:
			self._log("Workspace needs to be updated. Remote workspace version: %s" % v)
			self.update_projects(w)
			self.purge()
			self._log("Client updated successfuly! \n")

	def update_projects(self, workspace):
		self._log("Recreating local workspace...")
		shutil.rmtree(self._path)
		if not os.path.exists(self._path):
			os.makedirs(self._path)

		self._log("Downloading projects files. Please, be a little patient, it may take some time...")
		urlretrieve (workspace, self._local_workspace)

		self._log("Inflating workspace files...")
		self.unzip(self._local_workspace, self._path)
		os.remove(self._local_workspace)

		self._log("Workspace created and populated successfully!")

	def purge(self):
		self._log("Purging configuration files...")
		os.remove(self._local)

		self._log("Downloading untouched configuration file from server...")
		urlretrieve (self._remote, self._local)

	def get_remote_info(self, input, w = _main_workspace):
		xmldoc = minidom.parse(urlopen(input))
		config = xmldoc.getElementsByTagName("config")[0]

		if(len(xmldoc.getElementsByTagName("workspaces")) < 1 
			or len(xmldoc.getElementsByTagName("workspaces")[0].getElementsByTagName(w)) < 1):
			self._log("\nERROR: workspace not found in remote repository.")
			exit(0)

		return (str(self.handleTok(config.getElementsByTagName("version"))).strip().capitalize(),
		str(self.handleTok(xmldoc.getElementsByTagName(w))).strip().capitalize())

	def get_remote_version(self, input):
		(v, w) = self.get_remote_info(input)
		return v

	def get_local_version(self):
		xmldoc = minidom.parse(open(self._local, "r"))
		config = xmldoc.getElementsByTagName("config")[0]

		if(config):
			return str(self.handleTok(config.getElementsByTagName("version"))).strip().capitalize()
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
		self._log("    --version                  get local version")
		self._log("    --skip-update-check        skip remote check, just take me to the grefine")
		self._log("    --purge-installation       purge all stuff and redownload from remote")
		self._log("    --workspace [name]         specify remote workspace")
		self._log("    --directory [name]         specify local workspace")
		self._log("    --help                     SOS: help me")
		return

	def version(self):
		self._info()
		self._log("Local version: %s" % self.get_local_version())
		self._log("")
		return

	def remote_version(self):
		self._info()
		self._log("Local version: %s" % self.get_local_version())
		self._log("Remote version: %s" % self.get_remote_version(self._remote))
		self._log(("Client needs to be updated.", "Client is updated!")[self.get_local_version() == self.get_remote_version(self._remote)])
		self._log("")
		return

	def run(self):
		os.system('launcher -d %s'%self._path)		
		return

	def __init__(self):

		# --help
		if(len(sys.argv) > 1 and (sys.argv[1] == "--help" or sys.argv[1] == "-h" or sys.argv[1] == "help")):
			self._help()
			return

		# --version
		if(len(sys.argv) > 1 and (sys.argv[1] == "--version" or sys.argv[1] == "-v" or sys.argv[1] == "version")):
			self.version()
			return

		# --remote-version
		if(len(sys.argv) > 1 and (sys.argv[1] == "--remote-version" or sys.argv[1] == "-r" or sys.argv[1] == "remote")):
			self.remote_version()
			return

		self._info()

		# --purge-installation
		if(len(sys.argv) > 1 and (sys.argv[1] == "--purge-installation" or sys.argv[1] == "-p" or sys.argv[1] == "purge")):
			(v,w) = self.get_remote_info(self._remote)
			self.update_projects(w)
			self.purge()
			return

		# --workspace
		if(len(sys.argv) > 1 and (sys.argv[1] == "--workspace" or sys.argv[1] == "-w" or sys.argv[1] == "workspace")):

			if(len(sys.argv) < 2):
				self._log("You need to specify the workspace you want to use.")
				exit()

			(v,w) = self.get_remote_info(self._remote, sys.argv[2])
			self.update_projects(w)
			self.purge()
			self.run()
			return

		if(len(sys.argv) > 1 and sys.argv[1] == "--skip-update-check"):
			self.run()
			return

		if(len(sys.argv) > 1 and (sys.argv[1] == "--directory" or sys.argv[1] == "-d" or sys.argv[1] == "directory")):

			if(len(sys.argv) < 2):
				self._log("You need to specify the local directory you want to work on.")
				exit()

			self._path = sys.argv[2]
			return

		self.check_updates()
		self.run()

l = Launcher()