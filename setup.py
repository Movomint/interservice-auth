from setuptools import setup, find_packages

setup(
    name="internal-services-auth",
    version="0.1.0",
    packages=find_packages(where="."),
    install_requires=["PyJWT>=2.0", "fastapi"],
    python_requires=">=3.11",
)

