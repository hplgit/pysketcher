from distutils.core import setup
import pysketcher  # much easier when no lib dir
setup(name='pysketcher',
      version=pysketcher.__version__,
      url='',
      author=pysketcher.__author__,
      description='',
      license='BSD',
      long_description=pysketcher.__doc__,
      platforms='any',
      #package_data={'name': ['pysketcher/*.dat'],},
      packages=['pysketcher'])

