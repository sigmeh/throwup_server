<h4>throwup_server</h4>

throwup_server is a python module to generate a simple localhost server, serving from a specific "remote" directory on a given port. 

Usage:

	>>> from throwup_server import throwup_server
	>>> throwup_server.throwup( path-to-directory [,port=port] )
	
	$ python throwup_server.py [path-to-directory]


throwup_server.py copies the following files to the target directory:
	start_throwup.py	# invoke server script
	serve_throwup.py	# actual server
	throwup_filelist	# script for retrieving remote directory's contents
						#   accessed at http://127.0.0.0:PORT/throwup_filelist