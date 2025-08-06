from setuptools import setup, find_packages
from auth_lib import token

setup(
    name="internal-services-auth",
    version="0.1.0",
    author="Will Anderson",
    packages=find_packages(where="."),
    install_requires=["PyJWT>=2.0", "fastapi"],
    python_requires=">=3.11",
)

