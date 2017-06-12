#!/usr/bin/env python
'''
This script runs automatically from throwup_server.py via a subprocess call. 
This script starts the server located in a remote directory, where it has 
just been copied via the throwup_server.py script.

This script invokes the python server via a subprocess call to run
serve_throwup.py on the optionally-specified port. 
The port is an argument supplied to this program during its invocation.  

This script can optionally be run directly:
	$ python start_throwup.py [port]
	

'''

import subprocess as sp
import time
import requests
import sys


def start(**kwargs):
	''' Use start_throwup.start( port=port ) ''' 	
	
	port = kwargs.get('port') if kwargs.get('port') else '8002'

	try:
		'''
		serve_throwup.start_server( port=port )
		print 'serve'
		'''
		print 'Starting new localhost python server on port %s' %port
		cmd = ('python serve_throwup.py %s &' % port ).split()
		sp.Popen(cmd)
		
		time.sleep(.5)	
		
	except:
		time.sleep(.5)
		print 'Cannot start server.'
		
		
def main():

	port = sys.argv[1] if len(sys.argv) > 1 else None
	
	start( port=port )
		
if __name__ == '__main__':
	main()

