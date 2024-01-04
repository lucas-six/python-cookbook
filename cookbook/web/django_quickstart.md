# Django - Quick Start

[How to Read **"Django"**](https://lucas-six.github.io/python-cookbook/audios/django_pronunciation.mp3)

## Solution

```bash
pipenv install 'django~=4.2'

pipenv install --dev pylint-django
#pipenv install --dev flake8-django
```

### Create Project

Edit `pyproject.toml`

```toml
dependencies = [
    "django ~= 4.2",
    "django-stubs[compatible-mypy]",
]

[project.optional-dependencies]
test = [
    "pylint-django",
    # "flake8-django",

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

[tool.pylint.main]
load-plugins = [
    "pylint_django",
]

[tool.pylint.'MESSAGES CONTROL']
disable = [
    "django-not-configured",
]

#[tool.flake8]
#extend-exclude = "**/migrations/*.py"
#per-file-ignores = "settings.py:E501"
#require-plugins = "flake8-django"

[tool.pyright]
exclude = [
    "**/migrations",
]
ignore = [
    "**/models.py",
    "**/admin.py",
]
```

```yaml
# .pre-commit-config.yaml

# See https://pre-commit.com for more information
# See https://pre-commit.com/hooks.html for more hooks
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    hooks:
      - id: double-quote-string-fixer
        exclude: manage.py
      - id: name-tests-test
        args: [--django]
  - repo: https://github.com/pre-commit/mirrors-mypy
    hooks:
      - id: mypy
        exclude: (settings.py|manage.py|migrations/|models.py|admin.py)
  - repo: https://github.com/PyCQA/pylint
    hooks:
      - id: pylint
        additional_dependencies: [django, pylint-django]
        exclude: (settings.py|manage.py|migrations/|models.py|admin.py)
        args:
          - '--load-plugins=pylint_django'
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
4.2.7

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
