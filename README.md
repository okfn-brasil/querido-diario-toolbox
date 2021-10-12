# Querido Diário Toolbox

[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/querido-diario-toolbox)](https://pypi.org/project/querido-diario-toolbox/)
[![PyPI](https://img.shields.io/pypi/v/querido-diario-toolbox)](https://pypi.org/project/querido-diario-toolbox/)

O objetivo da `querido-diario-toolbox` é dar à comunidade do Querido Diário
o ferramental para executar suas próprias análises e manipulações com os dados
que são obtidos pelo QD. Além disso, a biblioteca também será
integrada nas aplicações utilizadas em produção pelo Querido Diário. Ou seja,
quem utilizar a biblioteca poderá reproduzir localmente as mesmas etapas de
processamento que o QD realiza.

A biblioteca dá diferentes níveis de abstrações para trabalhar com os
dados. Desde uma simples limpeza de texto a partir de strings até conversão de
arquivos de vários formatos para texto puro.


## Instalação

```sh
$ pip install querido-diario-toolbox
```

Atualmente, a `querido-diario-toolbox` é compatível com Python 3.8+.

Para executar extrações de texto é necessário ter o
[Tesseract OCR](https://tesseract-ocr.github.io/tessdoc/) instalado. Assim como
ter os `.jar` do
[Apache Tika](https://tika.apache.org/download.html) (última versão testada: 1.24.1)
e [Tabula](https://github.com/tabulapdf/tabula-java/releases) (última versão
testada: v1.0.4)
acessíveis para poder passar seus caminhos de arquivo como argumentos.

## Exemplos de uso

Exemplos mais elaborados estão disponíveis na pasta
[`./examples`](examples). Você pode visualizá-los (e interagir se desejar)
utilizando notebooks [Jupyter](https://jupyter.org/).

### Removendo espaços desnecessários em um texto

```python
In [1]: from querido_diario_toolbox.process.text_process import remove_breaks

In [2]: texto = "\n\n\nEste texto tem vários      espaços em branco\n\n \ndesnecessários.\n"

In [3]: remove_breaks(texto)
Out[3]: 'Este texto tem vários espaços em branco desnecessários.'
```

### Encontrando CNPJs válidos em um texto

```python
In [1]: from querido_diario_toolbox.process.edition_process import extract_and_validate_cnpj

In [2]: texto = "As empresas de CNPJ válidos 00.000.000/0001-91 e 00.360.305/0001-04 existem mas a de CNPJ 12.123.123
   ...: /1234.12 não existe..."

In [3]: extract_and_validate_cnpj(texto)
Out[3]: ['00.000.000/0001-91', '00.360.305/0001-04']
```

### Convertendo arquivo de formato fechado para texto puro e extraindo metadados

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

Após a execução de `extrator.load_content(diario)`, dois arquivos (um `.txt`
com o texto puro e um `.json` com os metadados) serão criados.

## Colaborando

Para saber como colaborar com o projeto, seja através de *Issues*, *Pull
Requests* ou interagindo com a comunidade, leia o
[documento de colaboração geral do Querido Diário](https://github.com/okfn-brasil/querido-diario-comunidade/blob/main/CONTRIBUTING.md)
e depois leia o
[documento de colaboração específico deste repositório](CONTRIBUTING.md).
