from setuptools import setup
install_reqs = parse_requirements('requirements.txt', session='hack')

setup(
   name='cisstm_sat',
   version='0.1',
   description='The CissTM Satellite, but now written in python.',
   author='Micha den Heijer',
   author_email='micha@michadenheijer.com',
   packages=['cisstm_sat'],
   install_requires=reqs
)