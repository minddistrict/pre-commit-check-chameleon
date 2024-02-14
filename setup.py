from setuptools import find_packages
from setuptools import setup

version = "1.0.dev0"


def read(fname):
    with open(fname) as f:
        return f.read()


setup(
    name="pre-commit-check-chameleon",
    version=version,
    description="Check Chameleon templates",
    long_description="\n\n".join([read("README.rst"), read("CHANGES.rst")]),
    project_urls={
        "Changelog": "https://github.com/minddistrict/pre-commit-check-chameleon/blob/master/CHANGES.rst",
        "Issue Tracker": "https://github.com/minddistrict/pre-commit-check-chameleon/issues",
        "Sources": "https://github.com/minddistrict/pre-commit-check-chameleon",
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Software Development :: Testing",
        "Topic :: Text Processing :: Markup :: HTML",
        "Topic :: Utilities",
    ],
    keywords="pre-commit chameleon",
    author="Minddistrict",
    author_email="support@minddistrict.com",
    package_dir={"": "src"},
    packages=find_packages("src"),
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.11",
    install_requires=[
        "lxml",
    ],
    extras_require={
        "test": [
            "testfixtures",
        ],
    },
    entry_points={
        "console_scripts": ["check-chameleon = check_chameleon.check_chameleon:main"]
    },
)
