#!/usr/bin/env python
'''
Start a python server in a remote directory on local machine
'''


def help(): print '''
#########################
### throwup_server.py ###
#########################

help menu: access via argument of -h, --h, -help, --help 
e.g.,
  $ python throwup_server.py -h
	or
  >>> throwup_server.help()

Start a python server in a remote directory on local machine

Usage:
  >>> import throwup_server
  >>> throwup_server.help()
  >>> throwup_server.throwup( path_to_dir=path_to_dir [, port=port])

	or

  $ python throwup_server.py [path_to_directory] [port]

1. Kill any running process with the name 'serve_throwup.py'
2. Copy server scripts to remote directory
3. Start server from remote directory
4. Test whether server is operational

These files are copied to the target directory:
  start_throwup.py	# invokes server script
  serve_throwup.py	# actual server
  filelist_throwup	# retrieves remote directory's contents
  			# access via http://127.0.0.1:port/filelist_throwup
			
#######################
'''

import sys
import time
import subprocess as sp
import requests
import pkgutil
import re
import json
import os


#
#
#
def bash(cmd, **shell):
	'''Issue subprocess calls from cmd (standard bash syntax)
	Determine whether cmd should be split (depending on whether shell=True)
	Print any error received and return the subprocess command's response	
	'''
	
	resp, err = sp.Popen(cmd if shell else cmd.split(' '), stdout=sp.PIPE, shell=shell).communicate()
	if err: 
		print 'Got error on command "%s":' % cmd
		print err
	return resp

#
#
#
def cleanup( **kwargs ):
	'''Find (and possibly kill) any serve_throwup.py process
	
	1. Test for active localhost server on specified kwarg 'port' using requests module
		Exception is raised if no server is active at localhost:port. The server can be started normally. 
	2. If no exception is raised, there is an active server at localhost:port
		Find the process that spawned the server (ps command) to get its pid
		Find the filesystem root directory (cwd) of the server 
		If the cwd of localhost:port/serve_throwup.py == kwarg path_to_dir (user-specified): do nothing
		Else: start server
	'''
	
	
	path_to_dir = kwargs['path_to_dir']
	port = kwargs.get('port')
	
	
	'''1. Test for active localhost server'''
	try:	
		#r = requests.get('http://localhost:%s' % port)
		r = requests.post('http://localhost:%s/throwup_options' % port, data = {'package':'pwd'})
	except Exception as e:
		print 'Found exception: \n\t'
		print  e
		print
		print 'No active server found at: http://localhost:%s ' % port
	else:
		print 'Found active server at: \n\t http://localhost:%s ' % port
		print 'Server responded with status: %s' % r.status_code
		
		
		# Find each serve_throwup.py process (ps command) and check server port
		# Get the process id (pid)
		# Use this pid to filter `lsof` results to obtain cwd from which the serve_throwup.py process was spawned
		
		'''
		cwd = json.loads(r.text)
		if cwd == path_to_dir:
			print 'localhost:%s/serve_throwup.py is already serving from the target directory.' % port
			print 'No new server will be started.'
			start_new_server = False
			return start_new_server
		'''
		
		
		cmd = 'ps -fA | grep serve_throwup'		# Leave off ".py" because this cmd becomes its own process (to filter later)
		result = [x.strip() for x in bash(cmd, shell=True).split('\n') if x]
		for line in result:
			if 'serve_throwup.py' in line:
				throwup_port = re.findall('serve_throwup.py\ (\d{4})',line)[0]	#check port number argument supplied to serve_throwup.py
			
				pid = [x for x in line.split(' ') if x][1]
				cmd = 'lsof -n | grep python | grep %s | grep cwd' % pid
				cwd_line = bash(cmd, shell=True)
		
				cwd = re.search('\/[\w\/]*', cwd_line).group()	#pull cwd from grep line
				
				if cwd == path_to_dir:
					print 'Current process serve_throwup.py (pid: %s) is already serving from the target directory.' % pid
					print 'No new server will be started.'
					start_new_server = False
					return start_new_server

	start_new_server = True
	return start_new_server
	
#		
#	
#
def test_server( path_to_dir, port ):
	''' Test that new server is running using requests module 
	The server requires some time to start up
	Server response is tested five times before giving up
	'''
	time.sleep(.5)
	try_count = 5
	
	while 1:
		try:
			r = requests.get('http://127.0.0.1:%s/' % port )
			print 'Received status code from server :',r.status_code
			print 'Server looks operational.'
			break
		except Exception as e:
			if try_count > 0:
				print 'Could not connect to server. Will retry %s times...' %try_count
				try_count -= 1
				time.sleep(.5)	
			else:
				print 'Error raised on server call with the following information:'
				print 'Note that requests module error #61 (connection refused) may occur if server is not yet running'
				print e
				break
	
	
#
#
#
def ask_ynq(msg):
	while 1:
		resp = raw_input( '%s (y n q): ' % msg )
		if resp in 'ynq':
			return resp
		else:
			print 'Bad input.'
			
#
#
#
def validate_port( port ):
	if not port:
		return 8002
	
	try:
		port = int(port)
		if not 1024 <= port <= 65535:
			raise Exception
			
	except Exception as e:
		print 'Bad port; Port must be a number between 1024-65535'
		print 'Omit port number from arguments to use default 8002'
		
		resp = ask_ynq('Use default port 8002 instead?')
		if resp in 'qn': 
			sys.exit()
			
		return 8002	# User responded with affirmative
	
	return port 	# Port appears ok
		
		
		
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
	port = validate_port( kwargs.get('port') ) 
	
	if not path_to_dir:
		print 'Need directory'
		return 'Need directory'
	path_to_dir = os.path.abspath(path_to_dir)
	
		
	#---------------------------------------------------
	# Identify any currently-running serve_throwup.py processes
	#	
	start_new_server = cleanup( path_to_dir=path_to_dir, port=port )
	if not start_new_server:
		print 'Cleanup function indicates that a server in the target directory'
		print 'is currently serving on the specified port.' 
		print 'Throwup_server is already operational. Initialization aborting.'
		sys.exit()
	
	
		
	#---------------------------------------------------
	# Read in file data via pkgutil (for copying to remote directory)
	#
	script_names = ['start_throwup.py', 'serve_throwup.py', 'filelist_throwup', 'throwup_options']
	
	try: 
		script_files = { x : pkgutil.get_data( 'throwup_server', x ) for x in script_names }
		
	except Exception as e:
		print 'Cannot locate script files for copying'
		print e
		sys.exit()	
	
		
	#---------------------------------------------------
	# Write file data to remote directory
	#			
	for script in script_files:
		with open( '%s/%s' % (path_to_dir, script) , 'w' ) as f:
			f.write( script_files[script] )

	time.sleep(.5)
	

	
	#------------------------------------------------------
	# Start server via call to remote-directory/start_throwup.py 
	#
	cmd = 'cd %s; chmod +x *throwup*; python start_throwup.py %s' % (path_to_dir, port)
	sp.Popen(cmd,shell=True)
	
	
	
	#-------------------------------------------------------
	# Test that new server is running
	#
	
	test_server( path_to_dir=path_to_dir, port=port )
	


def main():
	''' Retrieve path_to_dir argument and port number if supplied '''
	
	if len(sys.argv) == 1:
		print 'Need to specify directory.'
		print ' Use -----> $ python throwup_server.py path-to-directory'
		return 'Need to specify directory'	
	
	if sys.argv[1] in ['-h','--h','-help','--help']:
		return help()
			
	path_to_dir = sys.argv[1]
	
	port = sys.argv[2] if len(sys.argv) > 2 else None
	

	#
	#
	''' Start new server in target directory. The following functions are performed:
	1. cleanup	(kill active server)
	2. throwup	(copy server files and start server)
	3. test		(test server response)
	'''
	throwup( path_to_dir=path_to_dir, port=port )
	#
	#	

if __name__ == '__main__':
	main()
	