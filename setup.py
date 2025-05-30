import io
import os
import sys
from shutil import rmtree

from setuptools import Command, find_packages, setup

NAME = "querido-diario-toolbox"
DESCRIPTION = "Este projeto empodera quem deseja processar dados no contexto do Querido Diário e realizar suas próprias análises."
URL = "https://github.com/okfn-brasil/querido-diario-toolbox"
EMAIL = "queridodiario@ok.org.br"
AUTHOR = "Open Knowledge Brasil"
REQUIRES_PYTHON = ">=3.8.0"

# Pacotes obrigatórios
REQUIRED = ["python-magic", "python-slugify"]

# Pacotes extras
EXTRAS = {}

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

# README.md como descrição longa
try:
    with io.open(os.path.join(PROJECT_ROOT, "docs/README.md"), encoding="utf-8") as f:
        long_description = "\n" + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

about = {}

# Versão do pacote
project_slug = NAME.lower().replace("-", "_").replace(" ", "_")
with open(os.path.join(PROJECT_ROOT, project_slug, "__version__.py")) as f:
    exec(f.read(), about)


class AuxiliaryCommand(Command):
    """Apoia a publicação com o setup.py"""

    description = "Build and publish the package."
    user_options = []

    @staticmethod
    def status(s):
        """Imprime em negrito"""
        print("\033[1m{0}\033[0m".format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def reset_build(self):
        try:
            self.status("Removing previous builds…")
            rmtree(os.path.join(PROJECT_ROOT, "dist"))
        except OSError:
            pass

        self.status("Building Source and Wheel (universal) distribution…")
        os.system("{0} setup.py sdist bdist_wheel --universal".format(sys.executable))


class TestUploadCommand(AuxiliaryCommand):
    def run(self):
        self.reset_build()

        self.status("Uploading the package to TestPyPI via Twine…")
        os.system("twine upload --repository testpypi dist/*")

        sys.exit()


class UploadCommand(AuxiliaryCommand):
    def run(self):
        self.reset_build()

        self.status("Uploading the package to PyPI via Twine…")
        os.system("twine upload dist/*")

        self.status("Pushing git tags…")
        os.system("git tag v{0}".format(about["__version__"]))
        os.system("git push --tags")

        sys.exit()


setup(
    name=NAME,
    version=about["__version__"],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(exclude=["tests"]),
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    include_package_data=True,
    license="MIT",
    classifiers=[
        # Lista completa: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    cmdclass={
        "upload": UploadCommand,
        "test_upload": TestUploadCommand,
    },
)
