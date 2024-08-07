from setuptools import setup

setup(
    name='eurostatpy',
    version='0.9.1',
    description='Basic package for querying & downloading EuroStat data by dataset name or ID.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=['pandas', 'terminaltables', 'aiohttp']
)
