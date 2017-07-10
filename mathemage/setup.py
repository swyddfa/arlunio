from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='mage',
      version='0.1.1',
      description='A DSL/Framework for the creation of images',
      long_description=readme(),
      classifiers=[
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3 :: Only',
          'Topic :: Multimedia :: Graphics'
      ],
      author='Alex, Carney',
      author_email='alcarneyme@gmail.com',
      license='MIT',
      packages=['mage'],
      install_requires=[
          'matplotlib',
          'numpy',
          'Pillow',
          'scipy',
          'tqdm'
      ],
      setup_requires=['pytest-runner'],
      test_suite='tests',
      tests_require=['pytest', 'hypothesis'],
      include_package_data=True,
      zip_safe=False)
