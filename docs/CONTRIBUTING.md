**Português (BR)** | [English (US)](/docs/CONTRIBUTING-en-US.md)

# Contribuindo
O Querido Diário possui um [Guia para Contribuição](https://github.com/okfn-brasil/querido-diario-comunidade/blob/main/.github/CONTRIBUTING.md#contribuindo) principal que é relevante para todos os seus repositórios. Este guia traz informações gerais sobre como interagir com o projeto, o código de conduta que você adere ao contribuir, a lista de repositórios do ecossistema e as primeiras ações que você pode tomar. Recomendamos sua leitura antes de continuar.

Já leu? Então vamos às informações específicas deste repositório:
- [Desafios](#desafios)
- [Como configurar o ambiente de desenvolvimento](#como-configurar-o-ambiente-de-desenvolvimento)
    - [Em Linux](#em-linux)
- [Testes](#testes)
- [Mantendo](#mantendo)

## Desafios

## Como configurar o ambiente de desenvolvimento
### Em Linux
1. Antes de começar a desenvolver, confira se o [Tesseract OCR](https://tesseract-ocr.github.io/tessdoc/) está instalado.

2. Este repositório utiliza ambientes virtuais do Python para isolar seu ambiente de desenvolvimento, `pre-commit` para formatação de código e também [Apache Tika](https://tika.apache.org/download.html) (v1.24.1+) e [Tabula](https://github.com/tabulapdf/tabula-java/releases) (v1.0.4+) na execução de algumas funcionalidades da biblioteca. Ao executar o comando a seguir, você terá tudo isso configurado:

```sh
make setup
```

3. Ative o ambiente de desenvolvimento:

```sh
$ source .venv/bin/activate
```

## Testes
Você deve executar os testes com o comando a seguir:

```sh
$ make test
```

O repositório não deveria ter funcionalidades sem testes, quando for modificar algo, verifique se a cobertura de testes ainda está completa com:

```sh
$ make coverage
```

A formatação do código sempre será mantida pelo `pre-commit` ao realizar commits no projeto. Se desejar verificar se o código que está sendo desenvolvido está formatado adequadamente execute o comando a seguir:

```sh
$ make check
```

E este comando para que as formatações sejam efetuadas sem o auxílio do `pre-commit`.

```sh
$ make format
```

# Mantendo
As pessoas mantenedoras devem seguir as diretrizes do [Guia para Mantenedoras](https://github.com/okfn-brasil/querido-diario-comunidade/blob/main/.github/CONTRIBUTING.md#mantendo) do Querido Diário.