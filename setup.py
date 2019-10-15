import os
from setuptools import find_packages, setup
from drf_firebase import __version__

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
	README = readme.read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
	name='drf-firebase-authentication',
	version=__version__,
	packages=find_packages(),
	include_package_data=True,
	license='MIT License',
	description='A flexible Django Rest Framework Firebase authentication class',
	long_description=README,
	long_description_content_type='text/markdown',
	url='https://github.com/DoctorJohn/drf-firebase-authentication',
	author='Jonathan Ehwald',
	author_email='pypi@ehwald.info',
    install_requires=[
		'firebase-admin~=2.14.0',
		'djangorestframework>=3.1',
		'Django>=1.11',
	],
	classifiers=[
		'Environment :: Web Environment',
		'Framework :: Django',
		'Framework :: Django :: 1.11',
		'Framework :: Django :: 2.0',
		'Framework :: Django :: 2.1',
		'Framework :: Django :: 2.2',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: MIT License',
		'Operating System :: OS Independent',
		'Programming Language :: Python',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.3',
		'Programming Language :: Python :: 3.4',
		'Programming Language :: Python :: 3.5',
		'Programming Language :: Python :: 3.6',
		'Programming Language :: Python :: 3.7',
		'Topic :: Internet :: WWW/HTTP',
	],
)
