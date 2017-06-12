#!/usr/bin/env python

'''
Generate .tar.gz using `python setup.py sdist`
Install from this script using `python setup.py install`
'''

from setuptools import setup
def main():
	setup(
		name	= 'throwup_server',
		version	= '0.1',
		packages= ['throwup_server'],
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