# Python Project

## Setup Environment

### `uv`

```bash
uv init --python 3.12
uv add --dev black isort mypy pylint
```

### `Pipenv`

```bash
pipenv --python 3.12
pipenv install --dev black isort mypy pylint
```

## `pyproject.toml`

```ini
[project]
name = "<project_name>"
description = "<project description>"
authors = [
    {name = "<Author Name>", email = "<author@email>"},
    {name = "Lucas", email = "lucassix.lee@gmail.com"},
]
readme = "README.md"
requires-python = "~=3.12"
license-files = ["LICEN[CS]E*", "vendored/licenses/*.txt", "AUTHORS.md"]
maintainers = [
    {name = "<Maintainer Name>", email = "<maintainer@email>"},
]
keywords = ["xxx"]
# See https://pypi.org/classifiers/
classifiers = [
    "Development Status :: 2 - Pre-Alpha",

    "Intended Audience :: Developers",
    "Topic :: Software Development :: Documentation",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Topic :: Utilities",

    "Programming Language :: Python :: 3 :: Only",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: Implementation :: CPython",
    "Operating System :: OS Independent",
    ; "Framework :: Django :: 4",
    ; "Framework :: Django :: 4.2",
    "Private :: Do Not Upload",
    "Typing :: Typed",
]
dependencies = [
    "psycopg2 >= 2.8",

    "requests >=2.6",
    "configparser; python_version == '2.7'",
]
dynamic = ["version"]

#[project.optional-dependencies]
#doc = []

[project.urls]
Home = "<URL>"
Documentation = "<URL>"
Repository = "<URL>"

[tool.setuptools]
py-modules = ['src', 'app']

[[tool.uv.index]]
url = "https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple"
default = true

[dependency-groups]
dev = [
    "black>=25.1.0",
    "isort>=6.0.1",
    "mypy>=1.15.0",
    "pylint>=3.3.6",
]

[tool.black]
line-length = 100
target-version = ['py311', 'py312']
skip-string-normalization = true
include = '\.pyi?$'
extend-exclude = '''
tests/.*\.py$
'''

[tool.isort]
src_paths = ["src"]
atomic = true
profile = "black"
# skip = [
#    '.bzr',
#    '.direnv',
#    '.eggs',
#    '.git',
#    '.hg',
#    '.mypy_cache',
#    '.nox',
#    '.pants.d',
#    '.svn',
#    '.tox',
#    '.venv',
#    '__pypackages__',
#    '_build',
#    'buck-out',
#    'build',
#    'dist',
#    'node_modules',
#    'venv'
# ]
skip_gitignore = true
extend_skip = [".gitignore", ".env", ".dockerignore"]
# skip_glob = []
extend_skip_glob = []

[tool.mypy]
python_version = "3.12"
exclude = [
    "test_main.py",
]
follow_imports = "silent"
warn_redundant_casts = true
warn_unused_ignores = true
warn_unused_configs = true
disallow_any_generics = false
check_untyped_defs = true
no_implicit_reexport = true
disallow_untyped_defs = true

[tool.pylint.main]
recursive = true
py-version = 3.12
jobs = 0
ignore = "CVS,.git,__pycache__,.venv,.tox,.mypy_cache,.pytest_cache,tests"
ignore-paths = "tests"
ignore-patterns = "test_.*.py"
load-plugins = [
    "pylint.extensions.bad_builtin",
]

[tool.pylint.'FORMAT']
max-line-length = 100

[tool.pylint.'LOGGING']
logging-format-style = "new"

[tool.pylint.'MESSAGES CONTROL']
disable = [
    "raw-checker-failed",
    "bad-inline-option",
    "locally-disabled",
    "file-ignored",
    "suppressed-message",
    "deprecated-pragma",
    "use-symbolic-message-instead",
    "logging-fstring-interpolation",
    "too-many-positional-arguments",
    #"missing-class-docstring",
    #"missing-function-docstring",
]
enable = [
    "c-extension-no-member",
    "useless-suppression",
    "logging-format-interpolation",
    "duplicate-code",
]

[tool.pylint.design]
max-args = 15
min-public-methods = 0
max-locals = 25

[tool.pylint.deprecated_builtins]
bad-functions = ["map", "filter"]

[tool.pyright]
include = [
    "src",
]
exclude = [
    ".git",
    "**/__pycache__",
    "**/.venv",
    "**/.tox",
    "**/.mypy_cache",
    "**/.pytest_cache",
]
reportGeneralTypeIssues = "none"
reportUnboundVariable = "none"
stubPath = ""
pythonVersion = "3.12"
```

## More

- [`uv` - Python Cookbook](pkg/uv)
- [`pipenv` - Python Cookbook](pkg/pipenv)

## References

- [Packaging Python Projects](https://packaging.python.org/en/latest/tutorials/packaging-projects/)
- [PEP 517 - A build-system independent format for source trees](https://peps.python.org/pep-0517/)
- [PEP 301 – Package Index and Metadata for Distutils](https://peps.python.org/pep-0301/)
- [PEP 518 – Specifying Minimum Build System Requirements for Python Projects](https://peps.python.org/pep-0518/)
- [Package Classifiers](https://pypi.org/classifiers/)
- [TOML Documentation](https://toml.io/en/)
- [`black` Documentation](https://black.readthedocs.io/en/stable/)
- [`isort` Documentation](https://pycqa.github.io/isort/)
- [`mypy` Documentation](https://mypy.readthedocs.io/en/stable/)
- [`pylint` Documentation](https://pylint.pycqa.org/en/latest/)
