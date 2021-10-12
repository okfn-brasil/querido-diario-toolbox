from distutils.core import setup

from setuptools import find_packages

setup(
    name="querido-diario-toolbox",
    description="Querido Diário Toolbox",
    long_description=(
        "The goal of the `querido-diario-toolbox` is give the Querido Diário"
        "community the building blocks to perform its own analyses and manipulation in"
        "the data extracted by the Querido Diário project.  The lib should empowers the"
        "production applications used by the Querido Diário project to process the data"
        "as well as any other people which wants to perform their own analyses and"
        "run scripts."
    ),
    packages=find_packages(exclude=("tests",)),
    install_requires=["python-magic"],
    url="https://github.com/okfn-brasil/querido-diario-toolbox",
)
