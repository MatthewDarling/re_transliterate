from setuptools import setup

setup(
    name='re_transliterate',
    version='1.3',
    url="https://github.com/MatthewDarling/re_transliterate/",
    py_modules=['re_transliterate'],
    include_package_data=True,

    #Metadata
    description='Functions for transliteration using regular expressions',
    long_description=(open('readme.rst').read() + '\n\n' +
                      open('CHANGELOG.rst').read()),
    license='http://opensource.org/licenses/MIT',
    author='Matthew Darling',
    author_email='matthewjdarling@gmail.com',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering'],
)