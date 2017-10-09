from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


exec(open('stylo/version.py', 'r').read())

setup(name='stylo',
      version=__version__,
      description='Using a blend of Python and Maths for the '
      'creation of images',
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
      packages=['stylo'],
      install_requires=[
          'matplotlib',
          'numpy',
          'Pillow',
          'scipy'
      ],
      setup_requires=['pytest-runner'],
      test_suite='tests',
      tests_require=['pytest',
                     'hypothesis'],
      python_requires='>=3.0',
      include_package_data=True,
      zip_safe=False)
