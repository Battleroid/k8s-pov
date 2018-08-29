from setuptools import find_packages, setup
from view import __version__ as pov_version

setup(
    name='k8s-pov',
    author='Casey Weed',
    author_email='cweed@caseyweed.com',
    version=pov_version,
    description='Get map of pods to nodes',
    url='https://github.com/battleroid/k8s-pov',
    py_modules=['view'],
    install_requires=[
        'click',
        'tabulate'
    ],
    entry_points="""
        [console_scripts]
        k8s-pov=view:main
    """
)
