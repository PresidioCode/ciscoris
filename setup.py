from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="ciscoris",
    version="0.0.4",
    author="Jeff Levensailor",
    author_email="jeff@levensailor.com",
    description="Cisco CUCM RIS Library. Simple to use.",
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/levensailor/ciscoris",
    keywords=['Cisco', 'Call Manager', 'CUCM', 'RIS', 'LogCollection', 'VoIP'],
    packages=['ciscoris'],
    include_package_data=True,
    install_requires = [
    'suds-jurko==0.6',
    'urllib3==1.23'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)