from setuptools import setup

setup(name='gem_database',
      version='0.1.3',
      description='Database layer for GEM platform project',
      url='https://github.com/gem-platform/gem',
      author='Advaita Krishna das',
      author_email='advaita.krishna.das@gmail.com',
      license='MIT',
      packages=['gem', 'gem.db'],
      #setup_requires=[
      #    'pytest-runner'
      #],
      install_requires=[
          'pymongo',
      ],
      tests_require=[
          'pytest'
      ],
      zip_safe=False)
