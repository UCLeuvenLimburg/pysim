from setuptools import setup


def fetch_version():
      '''
      Fetches version variable from version.py
      '''
      version = {}

      with open('pysim/version.py') as f:
            exec(f.read(), version)

      return version['__version__']


setup(name='pysim',
      version=fetch_version(),
      description='Simulator',
      url='http://github.com/UCLeuvenLimburg/pysim',
      author='Frederic Vogels',
      author_email='frederic.vogels@ucll.be',
      license='MIT',
      packages=['pysim'],
      entry_points = {
            'console_scripts': [ 'pysim=pysim.command_line:shell_entry_point']
      },
      test_suite='nose.collector',
      tests_require=['nose'],
      zip_safe=False)
