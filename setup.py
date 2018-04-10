from pip.download import PipSession
from pip.req import parse_requirements
from setuptools import find_packages, setup
from view import __version__ as pov_version

reqs = parse_requirements('requirements.txt', session=PipSession())
requirements = [str(req.req) for req in reqs]

setup(
    name='k8s-pov',
    author='Casey Weed',
    author_email='cweed@caseyweed.com',
    version=pov_version,
    description='Get map of pods to nodes',
    url='https://github.com/battleroid/k8s-pov',
    packages=find_packages(),
    install_requires=requirements,
    entry_points="""
        [console_scripts]
        k8s-pov=view:main
    """
)
