#!/usr/bin/env python
'''
start_throwup.py runs automatically from throwup_server.py via 
a subprocess call. 

throwup_server.py copies these three files:
	start_throwup.py
	serve_throwup.py
	filelist_throwup.py
	
into the target directory, supplied as argument. 

start_throwup.py functions to start the server script (serve_throwup.py)
on an optionally-specified local port. 
	
This script can optionally be run directly:
	$ python start_throwup.py [port]

In this case, the server is started from the same 
directory (of start_throwup.py). 
Invoking a server directly in this way sidesteps instructions 
implemented in throwup_server.py, namely steps:
	1. Check for and kill any serve_throwup.py processes
		(2. is N/A)
	3. Test for active server
	
'''

import subprocess as sp
import time
import requests
import sys


def start(**kwargs):
	
	port = kwargs.get('port') if kwargs.get('port') else '8002'

	try:
		print 'Starting new localhost python server on port %s' %port
		cmd = ('python serve_throwup.py %s &' % port ).split()
		sp.Popen(cmd)

	except:
		
		print 'Cannot start server.'
		
		
def main():

	port = sys.argv[1] if len(sys.argv) > 1 else None
	start( port=port ) 
		
if __name__ == '__main__':
	main()

