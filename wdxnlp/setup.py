from setuptools import setup

setup(
    name='wdxnlp',
    version='0.1',
    py_modules=['wdxnlp'],
    include_package_data=True,
    install_requires=[
        'click',
    ],
    entry_points='''
        [console_scripts]
        wdxnlp=wdxnlp:cli
    ''',
)