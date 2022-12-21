# Django - Quick Start

[How to Read **"Django"**](https://leven-cn.github.io/python-cookbook/audios/django_pronunciation.mp3)

## Solution

```bash
pipenv install 'django~=3.2'
pipenv install --dev pylint-django flake8-django
```

### Create Project

Edit `pyproject.toml`

```toml
dependencies = [
    "django ~= 3.2",
]

[project.optional-dependencies]
test = [
    "pylint-django",
    "flake8-django",

    # "django-stubs[compatible-mypy]",
    # "django-types",
]

[tool.black]
extend-exclude = '''
migrations/.*\.py$
'''

[tool.isort]
extend_skip_glob = ["*/migrations/*"]

[tool.mypy]
exclude = [
    'settings.py',
    'migrations/',
    'models.py',
    'admin.py',
]

[tool.flake8]
extend-exclude = "**/migrations/*.py"
per-file-ignores = "settings.py:E501"
require-plugins = "flake8-django"

[tool.pyright]
include = [
    "examples"
]
exclude = [
    ".git",
    "**/__pycache__",
    "**/migrations",
]
ignore = [
    "**/models.py",
    "**/admin.py",
]
stubPath = ""
pythonVersion = "3.9"
```

```yaml
# .pre-commit-config.yaml

# See https://pre-commit.com for more information
# See https://pre-commit.com/hooks.html for more hooks
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
        args: [--markdown-linebreak-ext=md]
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-json
      - id: check-toml
      - id: check-added-large-files
        args: ['--maxkb=500']
      - id: mixed-line-ending
      - id: fix-byte-order-marker
      - id: detect-private-key
      - id: double-quote-string-fixer
        exclude: manage.py
      - id: name-tests-test
        args: [--django]
  - repo: https://github.com/psf/black
    rev: 22.12.0
    hooks:
      - id: black
        exclude: migrations/
        args: ['--verbose']
        # It is recommended to specify the latest version of Python
        # supported by your project here, or alternatively use
        # pre-commit's default_language_version, see
        # https://pre-commit.com/#top_level-default_language_version
        language_version: python3.10
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v0.991
    hooks:
      - id: mypy
        exclude: (settings.py|manage.py|migrations/|models.py|admin.py)
        additional_dependencies: [pydantic, types-redis]
        language_version: python3.10
  - repo: https://github.com/PyCQA/pylint
    rev: v2.15.9
    hooks:
      - id: pylint
        additional_dependencies: [django, pylint-django]
        exclude: (settings.py|manage.py|migrations/|models.py|admin.py)
        language_version: python3.10
  - repo: https://github.com/PyCQA/flake8
    rev: 5.0.4
    hooks:
      - id: flake8
        additional_dependencies: [flake8-django]
        exclude: migrations/
        args:
          [
            '--per-file-ignores',
            'settings.py:E501',
            '--require-plugins',
            'flake8-django',
          ]
```

```bash
$ pipenv run django-admin version
3.2.15

pipenv run django-admin startproject <project_name>
```

Edit `settings.py`:

```python
LANGUAGE_CODE = 'zh-hans'  # 'en-us'
TIME_ZONE = 'Asia/Shanghai'  # 'UTC'
```

Run:

```bash
pipenv run python manage.py makemigrations
pipenv run python manage.py migrate

pipenv run python manage.py createsuperuser

pipenv run python manage.py runserver [localhost:8000]
```

### Create App

```python
pipenv run python manage.py startapp <app_name>
```

- Edit `models.py`
- Edit `admin.py`
- Edit `views.py`
- Edit `tests.py`
- Edit `urls.py`

Edit `settings.py`

```python
INSTALLED_APPS = [
    <app_name>,
]
```

```bash
pipenv run python manage.py makemigrations [<app_name>]
pipenv run python manage.py migrate
```

## References

- [Django Documentation](https://docs.djangoproject.com/)
- [`django-stubs` PyPI](https://pypi.org/project/django-stubs/)
