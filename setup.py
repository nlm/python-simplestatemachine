from setuptools import setup,find_packages
from simplestatemachine import __version__

setup(
    name="simplestatemachine",
    version=__version__,
    packages=find_packages("simplestatemachine"),
    author="Nicolas Limage",
    author_email="github@xephon.org",
    description="simple state machine",
    license="GPL",
    keywords="state machine",
    url="https://github.com/nlm/python-simplestatemachine",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    setup_requires=[
        'nose>=1.0',
    ],
    test_suite="test_simplestatemachine",
)
