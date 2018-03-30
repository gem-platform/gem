from setuptools import setup

setup(name='gem_core',
      version='0.2',
      description='Core layer for GEM platform project',
      url='https://github.com/gem-platform/gem',
      author='Advaita Krishna das',
      author_email='advaita.krishna.das@gmail.com',
      license='MIT',
      packages=['gem', 'gem.core'],
      #setup_requires=[
      #    'pytest-runner'
      #],
      install_requires=[],
      tests_require=[
          'pytest'
      ],
      zip_safe=False)
