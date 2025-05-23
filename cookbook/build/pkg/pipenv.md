# Pipenv

The virtual environment manager for Python, with *`pip`* and *`venv`*.

```bash
pipx install pipenv
```

or

```bash
pip install pipenv
```

## Create Virtual Environments

```bash
cd <project-dir>
pipenv --python <x.y>

# For example:
pipenv --python 3.12

# or default version:
pipenv --three
```

## Remove Virtual Environments

```bash
pipenv --rm
```

## Install Packages/Dependencies

```bash
pipenv install <pkg ...>
pipenv install --dev <pkg ...>  # for development
```

## Install All Packages/Dependencies

```bash
pipenv install
```

If you want to install a local `setup.py`:

```bash
pipenv install -e .
```

## Uninstall Packages/Dependencies

```bash
pipenv uninstall <pkg ...>
pipenv uninstall --dev <pkg ...>  # for development
```

## Upgrade All Packages/Dependencies

```bash
pipenv update
```

## Run

```bash
pipenv run <python-cmd>
```

Examples:

```bash
pipenv run python a.py

pipenv run django-admin startproject a
pipenv run python manage.py runserver

pipenv run uwsgi a.ini
```

## Deploy a Project

```bash
pipenv sync
```

## Package Indexes (Mirror)

```bash
pipenv --pypi-mirror https://mirrors.aliyun.com/pypi/simple/ <cmd>
```

## References

- [`Pipenv` Documentation](https://pipenv.pypa.io/en/latest/)
- [Python - `venv` module](https://docs.python.org/3/library/venv.html)
- [PEP 405 – Python Virtual Environments](https://peps.python.org/pep-0405/)
