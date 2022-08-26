# Django - Quick Start

[How to Read **"Django"**](https://leven-cn.github.io/python-cookbook/audios/django_pronunciation.mp3)

## Solution

### Create Project

Edit `pyproject.toml`

```toml
dependencies = [
    "django ~= 3.2",
]

[project.optional-dependencies]
test = [
    "flake8-django",
    "django-stubs[compatible-mypy]",
    "django-types",
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

```bash
pipenv install 'django~=3.2'
pipenv install --dev flake8-django 'django-stubs[compatible-mypy]>=1.12' django-types

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
