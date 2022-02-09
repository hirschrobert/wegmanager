from setuptools import setup, find_packages


VERSION = '0.0.dev1'

install_requires = [
    'sqlalchemy == 1.4.29',
    'fints == 3.0.1',
    'Pillow == 9.0.0',
    'tkcalendar = 1.6.1',
]

docs_extras = [
    'Sphinx >= 4.3.2',  # Force RTD to use >= 4.3.2
    'docutils >=0.17.1',
]

data_files = [
    ('config', ['data/config.sample.ini']),
    ('config', ['data/bank_attributes.json']),
    ('share/applications/', ['wegmanager/wegmanager.desktop']),
    ('lib/python3.8/site-packages/wegmanager', ['wegmanager/icon.png']),
    ('', ['debian/start.sh']),
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
    package_dir={'wegmanager': 'wegmanager'},
    packages=find_packages(),
    package_data={'wegmanager': ['locale/*/LC_MESSAGES/*.mo']},
    entry_points={
        'gui_scripts': ['wegmanager = wegmanager.wegmanager:main']
    },
    data_files=data_files,
    python_requires='>=3.8',
    install_requires=install_requires,
    extras_require={'docs': docs_extras}
)
