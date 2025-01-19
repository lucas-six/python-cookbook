# Python Project

## Setup Environment

```bash
pipenv --python 3.11
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
requires-python = "~=3.11"
license = {file = "LICENSE"}
maintainers = [
    {name = "<Maintainer Name>", email = "<maintainer@email>"},
]
keywords = ["xxx"]
classifiers = [
    "Development Status :: 1 - Planning",
    "Programming Language :: Python :: 3 :: Only",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: Implementation :: CPython",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Topic :: Utilities",
    "Operating System :: OS Independent",
    "License :: OSI Approved :: MIT License",
    "License :: OSI Approved :: Apache Software License",
    "Typing :: Typed",
]
dependencies = [
    "psycopg2 >= 2.8",
    "redis >= 4.0",
    "types-redis",

    "requests >=2.6",
    "configparser; python_version == '2.7'",
]
dynamic = ["version"]

[project.optional-dependencies]
test = [
    "black",
    "isort",
    "mymy",
    "pylint",
]
doc = []

[project.urls]
Home = "<URL>"
Documentation = "<URL>"
Source = "<URL>"

[tool.black]
line-length = 88
target-version = ['py310', 'py311']
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
python_version = "3.11"
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
py-version = 3.11
jobs = 0
ignore = "CVS,.git,__pycache__,.mypy_cache,tests"
ignore-paths = "tests"
ignore-patterns = "test_.*.py"
load-plugins = [
    "pylint.extensions.bad_builtin",
]

[tool.pylint.'FORMAT']
max-line-length = 88

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
    #"duplicate-code",
]
enable = [
    "c-extension-no-member",
    "useless-suppression",
    "logging-format-interpolation",
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
    "**/.mypy_cache",
]
reportGeneralTypeIssues = "none"
reportUnboundVariable = "none"
stubPath = ""
pythonVersion = "3.11"
```

## More

- [`pipenv` - Python Cookbook](pkg/pipenv)

## References

- [Packaging Python Projects](https://packaging.python.org/en/latest/tutorials/packaging-projects/)
- [`black` Documentation](https://black.readthedocs.io/en/stable/)
- [`isort` Documentation](https://pycqa.github.io/isort/)
- [`mypy` Documentation](https://mypy.readthedocs.io/en/stable/)
- [`pylint` Documentation](https://pylint.pycqa.org/en/latest/)
