#!/usr/bin/env python

'''
Install from this script using the command `python setup.py install`
	-or-
Generate .tar.gz using `python setup.py sdist`

'''

import subprocess as sp
from setuptools import setup
import sys
import time
	
def main():

	setup(
		name			= 'throwup_server',
		version			= '0.1',
		packages		= ['throwup_server'],
		package_data	= {'throwup_server' : ['filelist_throwup']},
		#install_requires	= [''],	
		
		author			= 'sigmeh',
		author_email	= '',
		description		= '',
		license 		= '',
		keywords		= '',
		url				= '',
		
	)

if __name__ == '__main__':
	main()