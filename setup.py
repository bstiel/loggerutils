from setuptools import setup

setup(name='loggingutils',
      version='0.1.0',
      description='Celery optimised log formatter',
      url='http://github.com/bstiel/loggingutils',
      author='Bjoern Stiel',
      author_email='bjoern.stiel@distributedpython.com',
      license='BSD-3-Clause',
      packages=['loggingutils'],
      python_requires=">=3.0",
      test_suite='nose.collector',
      tests_require=['nose'],
      install_requires=[
            'Jinja2'
      ],
      zip_safe=False)