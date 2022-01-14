from setuptools import setup

VERSION = '0.0.dev1'

docs_extras = [
    'Sphinx >= 4.3.2',  # Force RTD to use >= 4.3.2
    'docutils >=0.17.1',
]

setup(
    name='wegmanager',
    version=VERSION,
    description='accounting software for apartments in ownership communities.',
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
    keywords=["accounting", "apartment", "real estate"],
    author="Robert Hirsch",
    author_email="dev@robert-hirsch.de",
    url="https://github.com/hirschrobert/wegmanager",
    license="GPL-3.0-only",
    package_dir={'': 'src'},
    python_requires='>=3.8',
    extras_require={'docs': docs_extras},
)
