from setuptools import setup, find_packages

VERSION = (0, 1)

# Dynamically calculate the version based on VERSION tuple
if len(VERSION)>2 and VERSION[2] is not None:
    str_version = "%d.%d_%s" % VERSION[:3]
else:
    str_version = "%d.%d" % VERSION[:2]

version= str_version

setup(
    name = 'django-france-express',
    version = version,
    description = "Django app to get shipping prices from France Express (Geodis)",
    long_description = """django-france-express provides the ability to get prices from France Express shipping service.""",
    author = 'Julien Maupetit',
    author_email = 'julien.maupetit@comsource.fr',
	url = 'https://github.com/ComSource/django-france-express',
    license = 'GPL 3',
    platforms = ['any'],
    classifiers = [
		'Development Status :: 5 - Production/Stable',
		'Environment :: Web Environment',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: GNU General Public License (GPL)',
		'Operating System :: OS Independent',
		'Programming Language :: Python',
		'Framework :: Django'],
    packages = find_packages(),
    include_package_data = True,
)
