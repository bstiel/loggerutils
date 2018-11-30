from setuptools import setup

setup(name='loggerutils',
      version='0.3.0',
      description='Celery optimised log formatter',
      url='http://github.com/bstiel/loggerutils',
      author='Bjoern Stiel',
      author_email='bjoern.stiel@distributedpython.com',
      license='BSD-3-Clause',
      packages=['loggerutils'],
      python_requires=">=3.3",
      test_suite='nose.collector',
      tests_require=['nose'],
      install_requires=['Jinja2'],
      zip_safe=False)