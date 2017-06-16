# FontInstaller (by @olemoritz)

# This script installs a custom TTF font on iOS (system-wide).
# It can be used in one of two ways:

# 1. Simply run it in Pythonista, you'll be prompted for the URL of the font 
#    you'd like to install (if there's a URL in the clipboard, it'll be used by default)

# 2. Use it as an 'Open in...' handler, i.e. select this file in Pythonista's 'Open in...
#    menu' setting. This way, you can simply download a ttf file in Safari and open it in
#    Pythonista. The script will then automatically install the downloaded font.

# The script is inspired by the AnyFont app (https://itunes.apple.com/us/app/anyfont/id821560738)
# and the iOS integration of MyFonts (http://meta.myfonts.com/post/80802984786/install-fonts-from-myfonts-on-ios-7-devices)

import plistlib
import BaseHTTPServer
import webbrowser
import uuid
import urllib
import sys
import console
import clipboard
import os

# Request handler for serving the config profile:
class ConfigProfileHandler (BaseHTTPServer.BaseHTTPRequestHandler):
	config = None
	def do_GET(s):
		s.send_response(200)
		s.send_header('Content-Type', 'application/x-apple-aspen-config')
		s.end_headers()
		plist_string = plistlib.writePlistToString(ConfigProfileHandler.config)
		s.wfile.write(plist_string)
	def log_message(self, format, *args):
		pass

def run_server(config):
	ConfigProfileHandler.config = config
	server_address = ('', 0)
	httpd = BaseHTTPServer.HTTPServer(server_address, ConfigProfileHandler)
	sa = httpd.socket.getsockname()
	# Point Safari to the local http server:
	webbrowser.open('safari-http://localhost:' + str(sa[1]))
	# Handle a single request, then stop the server:
	httpd.handle_request()

class FontInstaller:
	
	def install(self, font_path):

		label = os.path.split(font_path)[1]
		
		extension = os.path.splitext(font_path)[1].lower()
		
		if extension != '.ttf':
			raise Exception('Not a ttf file.')
			
		with open(font_path, 'r') as f:
			
			font_data = f.read()
			
			# Create the configuration profile:
			unique_id = uuid.uuid4().urn[9:].upper()
			
			config = {'PayloadContent': [{
						'Font': plistlib.Data(font_data),
						'PayloadIdentifier': 'com.omz-software.font.' + unique_id, 
						'PayloadOrganization': 'omz:software', 
						'PayloadType': 'com.apple.font',
						'PayloadUUID': unique_id, 'PayloadVersion': 1}], 
						'PayloadDescription': label,
						'PayloadDisplayName': label,
						'PayloadIdentifier': 'com.omz-software.font.' + unique_id,
						'PayloadOrganization': 'omz:software', 
						'PayloadRemovalDisallowed': False, 
						'PayloadType': 'Configuration',
						'PayloadUUID': unique_id,
						'PayloadVersion': 1}
						
		run_server(config)
		
