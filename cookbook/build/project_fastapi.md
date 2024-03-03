# FastAPI Project

First, set up [Base Project](project).

## Setup Environment

```bash
pipenv install pydantic
pipenv install --dev pylint-pydantic

pipenv install fastapi[all]
pipenv install uvicorn[standard]

pipenv install motor  # MongoDB asyncio driver
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
    "pydantic",
    "fastapi[all]",
    "uvicorn[standard]",
    "motor",
]
dynamic = ["version"]

[project.optional-dependencies]
test = [
    "black",
    "isort",
    "mymy",
    "pylint",
    "pylint-pydantic",
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
migrations/.*\.py$
'''

[tool.isort]
src_paths = ["src", "app"]
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

[tool.mypy]
python_version = "3.11"
plugins = [
    "pydantic.mypy"
]
exclude = [
    "test_main.py",
]
follow_imports = "silent"
warn_redundant_casts = true
warn_unused_ignores = true
warn_unused_configs = true
disallow_any_generics = true
check_untyped_defs = true
no_implicit_reexport = true
disallow_untyped_defs = true

[tool.pydantic-mypy]
init_forbid_extra = true
init_typed = true
warn_required_dynamic_aliases = true
warn_untyped_fields = true

# mypy for MongoDB motor
[[tool.mypy.overrides]]
module = "motor.*"
ignore_missing_imports = true

[tool.pylint.main]
recursive = true
py-version = 3.11
jobs = 0
ignore = "CVS,.git,__pycache__,.mypy_cache,tests"
ignore-paths = "tests"
ignore-patterns = "test_.*.py"
ignored-classes = "Body"
extension-pkg-whitelist = "pydantic"
load-plugins = [
    "pylint.extensions.bad_builtin",
    "pylint_pydantic",
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
    "useless-suppression",
    "deprecated-pragma",
    "use-symbolic-message-instead",
    "logging-fstring-interpolation"
]
enable = [
    "c-extension-no-member",
]

[tool.pylint.design]
max-args = 12
min-public-methods = 1
max-locals = 22

[tool.pylint.deprecated_builtins]
bad-functions = ["map", "filter", "print"]

[tool.pyright]
include = [
    "src",
    "app",
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

## References

- [Python Project - Python Cookbook](project)
- [`Pydantic`](https://pydantic-docs.helpmanual.io/): data validation
