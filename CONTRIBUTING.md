# Colaborando

______________________________________

_[Click here](languages/en-US/CONTRIBUTING.md) to read this article in english._
______________________________________


Este projeto ainda está em fase inicial, então qualquer ideia e contribuição é
muito bem vinda. Se for possível e assim desejar, se engaje nas *Issues* e na
comunidade do projeto para fazermos esta construção coletivamente.

## Preparação do ambiente

Antes de começar a desenvolver, confira se o Tesseract OCR está instalado.

Este repositório utiliza ambientes virtuais do Python para isolar seu
ambiente de desenvolvimento, `pre-commit` para formatação de código e também
Apache Tika e Tabula na execução de algumas funcionalidades da biblioteca. Ao
executar o comando a seguir você terá tudo isso configurado:

```sh
$ make setup
```

Lembre-se de ativar o ambiente virtual:

```sh
$ source .venv/bin/activate
```

## Testes

Você deve executar os testes com o comando a seguir:

```sh
$ make test
```

O repositório não deveria ter funcionalidades sem testes, quando for modificar
algo, verifique se a cobertura de testes ainda está completa com:

```sh
$ make coverage
```

A formatação do código sempre será mantida pelo `pre-commit` ao realizar
commits no projeto. Se desejar verificar se o código que está sendo
desenvolvido está formatado adequadamente execute o comando a seguir:

```sh
$ make check
```

E este comando para que as formatações sejam efetuadas sem o auxílio do
`pre-commit`.

```sh
$ make format
```
