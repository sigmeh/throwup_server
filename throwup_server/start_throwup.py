#!/usr/bin/env python
'''
start_throwup.py runs the serve_throwup.py script, from 
within the target directory where they were just copied. 

Target directory is argument supplied to throwup_server.py, 
from command line invocation or module import
'''

import subprocess as sp
import time
import requests
import sys

def start(**kwargs):
	''' Use start_throwup.start( port=port ) ''' 	

	if not kwargs['port']:
		port = 8002
	
	try:
		print 'Starting new python server on port %s' %port
		cmd = 'python {{path_to_directory}}/serve_throwup.py &'.split()
		sp.Popen(cmd)
		time.sleep(.5)	
		
		#cmd = ('open http://localhost:%s/throwup_filelist' %port).split()
		#sp.Popen(cmd)	#open in default browser
		
	except:
		time.sleep(.5)
		print 'Cannot start server.'
		
		
def main():

	port = None
	if len(sys.argv) > 1:
		port = sys.argv[1]
	
	start(port=port)
	

		
if __name__ == '__main__':
	main()

