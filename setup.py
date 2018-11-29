from setuptools import setup

setup(name='funniest',
      version='0.1',
      description='Celery optimised log formatter',
      url='http://github.com/bstiel/loggingutils',
      author='Bjoern Stiel',
      author_email='bjoern.stiel@distributedpython.com',
      license='BSD-3-Clause',
      packages=['loggingutils'],
      test_suite='nose.collector',
      tests_require=['nose'],
      zip_safe=False)