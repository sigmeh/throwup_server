#!/usr/bin/env python
'''
Start a python server in a remote directory on local machine

Usage:
	>>> from throwup_server import throwup_server
	>>> throwup_server.throwup( path_to_dir=path_to_dir [, port=port])

	$ python throwup_server.py [path_to_directory] [port]

1. Kill any running process with the name 'serve_throwup.py'
2. Copy server scripts to remote directory
3. Start server from remote directory
4. Test whether server is operational

These files are copied to the target directory:
	start_throwup.py	# invoke server script
	serve_throwup.py	# actual server
	filelist_throwup	# script for retrieving remote directory's contents
						# 	accessed via http://127.0.0.1:port/filelist_throwup

'''

import sys
import time
import subprocess as sp
import requests
import pkgutil

#
#
#
def cleanup( **kwargs ):
	'''Find and kill any serve_throwup.py process'''
	
	path_to_dir = kwargs['path_to_dir']
	
	cmd = 'ps -fA | grep serve_throwup'
	result = [x for x in sp.Popen(cmd,stdout=sp.PIPE,shell=True).communicate()[0].split('\n') if x]
	for line in result:
		if 'serve_throwup.py' in line:
			pid = [x for x in line.split(' ') if x][1]
			print 'Found serve_throwup.py:'
			print line
			print 'Eliminating pid %s...' %pid,
			cmd = 'kill %s' %pid
			sp.Popen(cmd.split())
			print 'Done.'
			
#		
#	
#
def test_server( path_to_dir, port ):
	''' Test that new server is running using requests module '''
	time.sleep(1)
	
	try:
		r = requests.get('http://127.0.0.1:%s/' % port )
		print 'Received status code from server :',r.status_code
		print 'Server looks operational.'
	except Exception as e:
		print 'Error raised on server call with the following information:'
		raise e
		
#
#
#
def throwup( **kwargs ):
	'''Attempt to start server in remote directory via the following:
		1. run cleanup() to kill any server process currently running that is named serve_throwup.py
		2. read the following files and write their contents to the remote directory at path_to_dir:
			start_throwup.py	# script to start server
			serve_throwup.py	# server script
			filelist_throwup.py	# script to retrieve list of files in remote directory
		3. use requests module to test for active server at 127.0.0.1:port where port is kwarg or 8002 by default
	'''
	
	path_to_dir = kwargs.get('path_to_dir')
	port = kwargs.get('port') if kwargs.get('port') else '8002'
	
	if not path_to_dir:
		print 'Need directory'
		return 'Need directory'
	
	
	#	
	#------------------
	# Kill any server processes named serve_throwup.py
	#------------------
	#
	cleanup( path_to_dir=path_to_dir )
	
	
	#	
	#------------------
	# Read in file data via pkgutil (for copying to remote directory)
	#------------------
	#	
	script_names = ['start_throwup.py', 'serve_throwup.py', 'filelist_throwup']
	
	try: 
		script_files = { x : pkgutil.get_data( 'throwup_server', x ) for x in script_names }
		
	except Exception as e:
		print 'Cannot locate script files for copying'
		print e
		sys.exit()	
	
	
	#	
	#------------------
	# Write file data to remote directory
	#------------------
	#			
	for script in script_files:
		with open( '%s/%s' % (path_to_dir, script) , 'w' ) as f:
			f.write( script_files[script] )

	time.sleep(0.5)


	#	
	#------------------
	# Start server via call to remote-directory/start_throwup.py 
	#------------------
	#
	cmd = 'cd %s; chmod +x *throwup*; python start_throwup.py %s' % (path_to_dir, port)
	#cmd = 'cd %s; chmod +x *throwup*; python start_throwup.py port=%s' % ( path_to_dir, kwargs.get('port') )
	sp.Popen(cmd,shell=True)

	
	#	
	#------------------
	# Test that new server is running
	#------------------
	#
	
	test_server( path_to_dir=path_to_dir, port=port )
	


def main():
	''' Retrieve path_to_dir argument and port number if supplied '''
	
	if len(sys.argv) == 1:
		print 'Need directory'
		return 'Need directory'	
	
		
	path_to_dir = sys.argv[1]
	
	port = sys.argv[2] if len(sys.argv) == 3 else 8002

	#
	#
	''' Start new server in target directory'''
	throwup( path_to_dir=path_to_dir, port=port )
	#
	#	

if __name__ == '__main__':
	main()
	