import pathlib
from setuptools import setup


setup(
    name="dirlog",
    version="0.0.1",
    description="Directory logging utility library",
    long_description=pathlib.Path(__file__).parent.joinpath("README.md").read_text(),
    long_description_content_type="text/markdown",
    url="https://github.com/realpython/reader",
    author="Ismael Balafrej",
    author_email="ismael.balafrej@usherbrooke.ca",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["dirlog"],
    include_package_data=True,
    install_requires=["toml", "pandas"],
    entry_points={
        "console_scripts": [
            "dirlog=dirlog.__main__:main",
        ]
    },
)
