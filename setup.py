from setuptools import find_packages
from setuptools import setup

version = "1.0.dev0"

setup(
    name="pre-commit-check-chameleon",
    version=version,
    package_dir={"": "src"},
    packages=find_packages("src"),
    include_package_data=True,
    zip_safe=False,
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
