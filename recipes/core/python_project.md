# Setup Python Project

## Setup Environment

```bash
pipenv install --dev flake8 pytest coverage[toml] pytest-cov pre-commit pyupgrade
```

## `pyproject.toml`

```toml
[project]
dependencies = [
    "psycopg2 >= 2.8",
    "redis >= 4.0",

    "requests >=2.6",
    "configparser; python_version == '2.7'",
]
dynamic = ["version"]

[project.optional-dependencies]
test = [
    "flake8",
    "pytest",
    "coverage",
    "pytest-cov",
    "pre-commit",
    "pyupgrade",
]
doc = [
    "sphinx"
]

[project.scripts]
<command_name> = "xxx:main"

[project.gui-scripts]
<command_name> = "xxx:main_gui"

[project.entry-points."<group.name>"]
dogelang = "<package>:<name>"

[tool.black]
extend-exclude = '''
# A regex preceded with ^/ will apply only to files and directories
# in the root of the project.
^/foo.py  # exclude a file named foo.py in the root of the project (in addition to the defaults)
'''

[tool.mypy]
exclude = [
    '^file1\.py$',  # TOML literal string (single-quotes, no escaping necessary)
    "^file2\\.py$",  # TOML basic string (double-quotes, backslash and other characters need escaping)

    'settings.py',
    'migrations/',
    'models.py',
    'admin.py',
]

[tool.pylint.main]
ignore = "migrations"
load-plugins = "pylint_django"

[tool.flake8]
# exclude = .svn,CVS,.bzr,.hg,.git,__pycache__,.tox,.eggs,*.egg
extend-exclude = "**/migrations/*.py"
# ignore = E121,E123,E126,E226,E24,E704,W503,W504
per-file-ignores = "settings.py:E501"
max_complexity = 10
max-line-length = 88
show-source = true
benchmark = true
require-plugins = "flake8-django"

[tool.pytest.ini_options]
markers = [
    "slow: marks tests as slow (deselect with '-m \"not slow\"')",
    "serial",
]
addopts = [
    "--strict-markers",
    "--cov",
    "--cov-append",
    "--durations=5",
    "--durations-min=0.25",
]
norecursedirs = [
    ".git",
    ".*_cache",
    ".tox",
    "*.egg-info",
    "docs",
]

[tool.coverage.run]
parallel = true

[tool.coverage.report]
skip_empty = true
```

## `pre-commit`

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
  - repo: https://github.com/pycqa/isort
    rev: v5.11.3
    hooks:
      - id: isort
        name: isort (python)
        language_version: python3.10
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v0.991
    hooks:
      - id: mypy
        additional_dependencies: [pydantic, types-redis]
        language_version: python3.10
  - repo: https://github.com/PyCQA/pylint
    rev: v2.15.9
    hooks:
      - id: pylint
        language_version: python3.10
  - repo: https://github.com/PyCQA/flake8
    rev: 5.0.4
    hooks:
      - id: flake8
        args:
          [
            '--max-complexity',
            '10',
            '--max-line-length',
            '88',
          ]
  - repo: https://github.com/asottile/pyupgrade
    rev: v2.37.1
    hooks:
      - id: pyupgrade

default_language_version:
  # force all unspecified python hooks to run python3
  python: python3

ci:
  autofix_prs: true
  autofix_commit_msg: '[pre-commit.ci] auto fixes from pre-commit.com hooks'
  autoupdate_branch: ''
  autoupdate_commit_msg: '[pre-commit.ci] pre-commit autoupdate'
  autoupdate_schedule: weekly
  skip: []
  submodules: false
```

```bash
pre-commit install
```

## Git Pre-Commit

```bash
# .git/hooks/pre-commit
# chmod u+x .git/hooks/pre-commit

pipenv run isort .
pipenv run mypy .

# IDE may included
#pipenv run flake8 .
```

## GitHub Actions

### `pre-commit`

### GitHub Workflows

```yaml
# .github/workflows/lint.yml

name: lint

on:
  pull_request:
    branches:
      - 'main'

jobs:
  # Skip it when GitHub Actions of pre-commit has been configured.
  pre-commit:
    name: Run pre-commit
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: pre-commit/action@v3.0.0
```

## References

- [PEP 517 - A build-system independent format for source trees](https://peps.python.org/pep-0517/)
- [PEP 518 – Specifying Minimum Build System Requirements for Python Projects](https://peps.python.org/pep-0518/)
- [`flit` Documentation](https://flit.pypa.io/en/latest/)
- [TOML 1.0](https://toml.io/en/v1.0.0)
- [PEP 621 – Storing project metadata in pyproject.toml](https://peps.python.org/pep-0621/)
- [`pre-commit` Documentation](https://pre-commit.com/)
- [`flake8` Documentation](https://flake8.pycqa.org/en/latest/)
- [`pytest` Documentation](https://docs.pytest.org/)
- [`coverage` Documentation](https://coverage.readthedocs.io/)
