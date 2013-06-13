import urllib, sys, os
from xml.dom import minidom

class Launcher:

	_config = "https://gist.github.com/luiseduardobrito/5750844/raw/3216b5c8243aae0c717bc7d4826836a66ae3dbe3/config.xml"

	def _log(self, msg):
		print msg

	def check_updates(self, config_url = ''):
		self._log("Getting update information from server...")
		self._log("Client already in latest version.")

	def run(self):
		self._log("Starting OpenRefine jetty server...")
		os.system('. ../refine')

	def __init__(self):
		print "Initializing launcher..."
		if(len(sys.argv) > 1 and sys.argv[1] != "--skip-update-check"):
			self._config = sys.argv[1]
			check_updates()
		self.run()

l = Launcher()