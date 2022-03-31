# Contributing

This project is still in its early stages, so any ideas and contributions are more than welcome. If possible, and if you wish to, engage in *Issues* and in the project community to build this collaboratively.

## Preparing the environment

Before starting to develop, make sure Tesseract OCR is installed.

This repository uses Python virtual environments to isolate its
development environment, `pre-commit` for code formatting, and also
Apache Tika and Tabula in the execution of some functionalities of the library. By running the following command, you will have all this set up:

```sh
$make setup
```

Remember to activate the virtual environment:

```sh
$ source .venv/bin/activate
```

## Tests

You must run the tests with the following command:

```sh
$make test
```

The repository should not have untested functionality. When modifying
something, check if test coverage is complete with:

```sh
$make coverage
```

Code formatting will always be kept by `pre-commit` when performing
commits to the project. If you want to verify whether the code being
developed is properly formatted, run the following command:

```sh
$make check
```

Finally, run this command so that formatting is performed without the help of `pre-commit`.

```sh
$make format
```
