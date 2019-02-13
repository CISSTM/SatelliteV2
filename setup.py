from distutils.core import setup, Extension
setup(name = 'distance', version = '1.0',  \
   ext_modules = [Extension('distance', ['src/distance.c'])])