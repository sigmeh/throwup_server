<h4>throwup_server</h4>

throwup_server is a python module to generate a simple localhost server, serving from a specific "remote" directory on a given port. 

Usage:

	>>> from throwup_server import throwup_server
	>>> throwup_server.throwup( path_to_dir=path_to_dir [,port=port] )
	
	$ python throwup_server.py [path-to-directory] [port]


<h5>
1. Kill any running process with the name 'serve_throwup.py'

2. Copy server scripts to target remote directory

3. Start server from remote directory

4. Test whether server is operational
</h5>

These files are copied to the target directory:

	start_throwup.py    # invoke server script
	
	serve_throwup.py    # actual server
	
	filelist_throwup    # script for retrieving remote directory's contents
	    # 	accessed via http://127.0.0.1:port/throwup_filelist