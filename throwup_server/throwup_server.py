#!/usr/bin/env python
'''
Start a python server in a remote directory (supplied as argument)

Copy these files to target directory:
	start_throwup.py	# invoke server script
	serve_throwup.py	# actual server
	throwup_filelist	# script for retrieving remote directory's contents
						# 	accessed from http://127.0.0.1:port/throwup_filelist


Usage:
	>>> from throwup_server import throwup_server
	>>> throwup_server.throwup( path-to-directory )

	$ python throwup_server.py [path_to_directory]
	
'''
import sys
import time
import subprocess as sp

def throwup( *path_to_dir ):
	
	if not path_to_dir:
		print 'Need directory'
		return 'Need directory'
	
	path_to_dir = path_to_dir[0]
	
	#------------------
	# Read in file data 
	#------------------
	with open('serve_throwup.py','r') as f:
		serve_throwup = f.read()
		
	with open('start_throwup.py','r') as f:
		start_throwup = f.read().replace( '{{path_to_directory}}',path_to_dir )
	
	with open('throwup_filelist','r') as f:
		throwup_filelist = f.read()
	
	
	#------------------
	# Write file data
	#------------------
	serve_path = path_to_dir+'/serve_throwup.py'
	with open(serve_path,'w') as f:
		f.write(serve_throwup)
		
	start_path = path_to_dir+'/start_throwup.py'	
	with open(start_path,'w') as f:
		f.write(start_throwup)
	
	throwup_path = path_to_dir+'/throwup_filelist'
	with open(throwup_path,'w') as f:
		f.write(throwup_filelist)
	

	time.sleep(0.5)
	
	
	#cmd = ('cd %s; chmod +x *throwup*; python serve_throwup.py &' % ( path_to_dir )).split()
	#sp.Popen(cmd, shell=True)
	
	
	cmd = 'cd %s; chmod +x *throwup*; python start_throwup.py' % path_to_dir
	sp.Popen(cmd,shell=True)
	

def cleanup():
	'''Find and kill serve_throwup.py'''
	cmd = 'ps -fA | grep serve_throwup'
	result = [x for x in sp.Popen(cmd,stdout=sp.PIPE,shell=True).communicate()[0].split('\n') if x]
	for line in result:
		if 'serve_throwup.py' in line:
			pid = [x for x in line.split(' ') if x][1]
			cmd = 'kill %s' %pid
			sp.Popen(cmd.split())
			return
	
	
def main():
	''' Ensure filepath is included in function call '''
	if len(sys.argv) == 1:
		print 'Need directory'
		return 'Need directory'
	
	''' Kill any server processes named serve_throwup.py and start new server in target directory'''
	cleanup()
	throwup( sys.argv[1] )
		
		
	

	pass
if __name__ == '__main__':
	main()