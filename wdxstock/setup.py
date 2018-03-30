from setuptools import setup, find_packages

setup(
    name='wdxstock',
    version='0.1',
    py_modules=['wdxstock'],
    include_package_data=True,
    packages = find_packages(),
    install_requires=[
        'click',
    ],
    entry_points='''
        [console_scripts]
        wdxstock=wdxstock:cli
    ''',
)