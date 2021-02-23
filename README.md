# rh-var

Robinhood value at risk (VaR) estimator

![test](https://github.com/jaredrcleghorn/rh-var/actions/workflows/test.yml/badge.svg)

## Installation

You will need [Pipenv](https://pipenv.pypa.io/en/latest/). On [Mac](https://www.apple.com/mac/), you
can install Pipenv using [Homebrew](https://brew.sh). To install Homebrew, run

```shell
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Then, to install Pipenv, run

```shell
brew install pipenv
```

To install dependencies, move into the project folder and run

```shell
pipenv install
```

Next, fill out the `config.json` file with your Robinhood `username` and `password`. Finally, to
start the application, run

```shell
pipenv run start
```

## Contributing

To run tests, run

```shell
pipenv run test
```
