from setuptools import setup, find_packages

setup(
    name='sxtools', # SxTools!MANAGER
    version='1.2.0',
    license='GPLv3+',
    description='SxTools!MANAGER helps you to manage your scene collections',
    package_dir={'':'src'},
    packages=find_packages(where='src'),
    author='nschepsen',
    author_email='schepsen@web.de',
    url='https://github.com/nschepsen/sxtools',
    keywords='library, video, tools',
    entry_points={
        'console_scripts': ['sxtools=sxtools.main:main']},
    classifiers=[
        'Development Status :: 4 - Beta'
        'Environment :: Console',
        'Environment :: X11 Applications :: Qt',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'
        'Natural Language :: English',
        'Natural Language :: German',
        'Natural Language :: Italian',
        'Natural Language :: Russian',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Programming Language :: SQL',
        'Topic :: Desktop Environment',
        'Topic :: Desktop Environment :: File Managers',
        'Topic :: Home Automation',
        'Topic :: Multimedia :: Video :: Display', 'Topic :: Utilities'
        ]
)

# SxTools!MANAGER helps you to manage collections according to your wishes