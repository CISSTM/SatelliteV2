from distutils.core import setup, Extension
setup(name = 'cisstm', version = '1.0',  \
   ext_modules = [
      Extension('calc', ['src/calc.cpp'])
   ])