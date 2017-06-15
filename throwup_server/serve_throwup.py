#!/usr/bin/env python
import BaseHTTPServer
import CGIHTTPServer
import cgitb
import time
import subprocess as sp
import sys


def start_server( **kwargs ):
	#cgitb.enable()  # CGI error reporting enabled
	port = int(kwargs.get('port')) if kwargs.get('port') else 8002
	
	server=BaseHTTPServer.HTTPServer
	handler=CGIHTTPServer.CGIHTTPRequestHandler
	server_address=("", port)
	handler.cgi_directories=['/']

	httpd=server(server_address, handler)
	httpd.serve_forever()


def main():
	try:
		port = sys.argv[1]
		start_server( port=port )
		
		time.sleep(.5)
		
	except:
		
		py_proc = sp.Popen(['ps -fA | grep python'], stdout=sp.PIPE, shell=True).communicate()[0]
		serv_proc = sp.Popen(['ps -fA | grep server'], stdout=sp.PIPE, shell=True).communicate()[0]
		
		time.sleep(.5)
		
		print
		print 'Cannot start server...'
		print 'The following information is available:'
		print '#--------python processes--------#'
		print py_proc
		print '#--------------------------------#'
		print '#--------server processes--------#'
		print serv_proc
		print '#-----------------------------------#'
		print
		print 'Kill active server.py processes running elsewhere if necessary.'
		print
		
if __name__ == '__main__':
	main()