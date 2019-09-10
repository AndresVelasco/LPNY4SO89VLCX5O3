import setuptools
import os

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup (
    name="simplestreetmatch",
    version="0.0.1",                                                                                                                                                                                              
    author="Andres Velasco Garcia",                                                                                                                                                                               
    author_email="andresvelasco.me@gmail.com",                                                                                                                                                                    
    description="code challenge",                                                                                                                                                                                 
    long_description=long_description,                                                                                                                                                                            
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=[]
)

#url="https://github.com/AndresVelasco/J3dAnaF9EBzG9xDD",

