# Querido Diário Toolbox

[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/querido-diario-toolbox)](https://pypi.org/project/querido-diario-toolbox/)
[![PyPI](https://img.shields.io/pypi/v/querido-diario-toolbox)](https://pypi.org/project/querido-diario-toolbox/)

The `querido-diario-toolbox` aims to offer the Querido Diario (QD) community a tool to perform its own analysis with the data extracted from QD. In addition, the library will also be integrated with the applications used in production by Querido Diario. It means that whoever uses the library will be able to locally reproduce the same processing steps performed by QD.

The library provides different levels of abstraction for working with the data, from simple cleaning of text using strings to converting files of various formats into plain text.

## Installation

```sh
$ pip install querido-diario-toolbox
```

Currently, `querido-diario-toolbox` is compatible with Python 3.8+.

To perform text extractions, you will need to have the [Tesseract OCR](https://tesseract-ocr.github.io/tessdoc/) installed. It is also required to have the `.jar` of the [Apache Tika](https://tika.apache.org/download.html) (latest version tested: 1.24.1) and [Tabula](https://github.com/tabulapdf/tabula-java/releases) (latest version tested: v1.0.4) so that you can pass their file paths as arguments. 

## Usage examples

More elaborate examples are available in the folder [`./examples`](examples). You can view them (and interact with them if you wish) using [Jupyter](https://jupyter.org/) notebooks.

### Removing unnecessary spaces in the text

```python
In [1]: from querido_diario_toolbox.process.text_process import remove_breaks

In [2]: text = "\n\n\nThis text has lots         of unnecessary whitespace\n\n \n.\n"

In [3]: remove_breaks(text)
Out[3]: 'This text has lots of unnecessary whitespace.'
```

### Finding valid CNPJs in a text

(Note to the English version: CNPJ is the Brazilian National Registry Number for companies)

```python
In [1]: from querido_diario_toolbox.process.edition_process import extract_and_validate_cnpj

In [2]: text = "Companies with valid CNPJ 00.000.000/0001-91 and 00.360.305/0001-04 do exist, but the one with CNPJ 12.123.123/1234.12 does not..."

In [3]: extract_and_validate_cnpj(text)

Out[3]: ['00.000.000/0001-91', '00.360.305/0001-04']
```

### Converting closed format file to plain text and extracting metadata

```python
In [1]: from querido_diario_toolbox import Gazette
   ...: from querido_diario_toolbox.etl.text_extractor import create_text_extractor

In [2]: config = {"apache_tika_jar": "caminho/apache/tika/jar/tika-app-1.24.1.jar"}
   ...: extrator = create_text_extractor(config)

In [3]: diario = Gazette(filepath="caminho/diario/fechado/diario.pdf")

In [4]: extrator.extract_text(diario)
   ...: extrator.extract_metadata(diario)
   ...: extrator.load_content(diario)
```

After running `extractor.load_content(diario)`, two files (one `.txt` with the plain text and a `.json` with the metadata) will be created.

## Contributing

To find out how to collaborate with the project as a whole, either through *Issues*, *Pull Requests* or interacting with the community, read the [general collaboration document of Querido Diário](https://github.com/okfn-brasil/querido-diario-comunidade/blob/main/CONTRIBUTING.md) and then read the [specific collaboration document of this repository](languages/en-US/CONTRIBUTING.md).