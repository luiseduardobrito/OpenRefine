import urllib, sys, os
from xml.dom import minidom

class Launcher:

	_remote = "https://gist.github.com/luiseduardobrito/5750844/raw/3216b5c8243aae0c717bc7d4826836a66ae3dbe3/config.xml"
	_version = "0.1"

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
		config = self.parse(self._remote)
		self._log("Client version: %s" % self._version)

	def parse(self, input):
		xmldoc = minidom.parse(urllib.urlopen(input))
		config = xmldoc.getElementsByTagName("config")[0]

		if(config):
			self._version = self.handleTok(config.getElementsByTagName("version"))
		else:
			self._log("No configuration information found, downloading new one...");
			os.system("wget %s" % self._remote)
			check_updates()

	def _help(self):
		self._log("\nGPNX Refine - Customized large data manipulated solution")
		self._log("Copyright 2013 - GPNX Group")
		self._log("Redesigned by Luis Eduardo Brito <luis@gpnxgroup.com>")
		self._howto()
		return

	def _howto(self):
		self._log("\nHow to:")
		self._log("    python launcher.py [options]\n")
		self._log("Available options:")
		self._log("    --skip-update-check     skip remote check, just take me to the grefine")
		self._log("    --help                  SOS: help me")
		self._log("\n")

	def run(self):
		self._log("Starting OpenRefine jetty server...")
		#os.system('./refine')

	def __init__(self):

		if(len(sys.argv) > 1 and (sys.argv[1] == "--help" or sys.argv[1] == "-h" or sys.argv[1] == "help")):
			self._help()
			return

		self._log("GPNX Refine - Initializing launcher resources...")

		if(len(sys.argv) > 1 and sys.argv[1] == "--skip-update-check"):
			self.run()
			return

		self.check_updates()
		self.run()

l = Launcher()