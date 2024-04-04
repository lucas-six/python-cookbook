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

    "requests >=2.6",
    "configparser; python_version == '2.7'",
]
dynamic = ["version"]

[project.optional-dependencies]
test = [
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
```

```bash
pre-commit install
```

## Git Pre-Commit

```bash
# .git/hooks/pre-commit
# chmod u+x .git/hooks/pre-commit

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
