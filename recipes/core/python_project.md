# Setup Python Project

## Setup Environment

```bash
pipenv --python 3.9

pipenv install --dev black isort mypy 'flake8>=4.0' pyupgrade 'pytest>=7.1' 'coverage>=6.4' 'pytest-cov>=3.0'
```

## `pyproject.toml`

```toml
[project]
name = "<project_name>"
description = "<project description>"
authors = [
    {name = "<Author Name>", email = "<author@email>"},
    {name = "Lee", email = "leven.cn@gmail.com"},
]
readme = "README.md"
requires-python = "~=3.9"
license = {file = "LICENSE"}
maintainers = [
    {name = "<Maintainer Name>", email = "<maintainer@email>"},
]
keywords = ["xxx"]
classifiers = [
    "Development Status :: 1 - Planning",
    "Programming Language :: Python :: 3 :: Only",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: Implementation :: CPython",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Topic :: Utilities",
    "Operating System :: OS Independent",
    "License :: OSI Approved :: MIT License",
    "License :: OSI Approved :: Apache Software License",
    "Typing :: Typed",
]
dependencies = [
    "requests >=2.6",
    "configparser; python_version == '2.7'",
]
dynamic = ["version"]

[project.optional-dependencies]
test = [
    "black",
    "isort",
    "mymy",
    "flake8 >= 4.0",
    "pyupgrade",
    "pytest >= 7.1",
    "coverage >= 6.4",
    "pytest-cov >= 3.0",
]
doc = [
    "sphinx"
]

[project.urls]
Home = "<URL>"
Documentation = "<URL>"
Source = "<URL>"

[project.scripts]
<command_name> = "xxx:main"

[project.gui-scripts]
<command_name> = "xxx:main_gui"

[project.entry-points."<group.name>"]
dogelang = "<package>:<name>"

[tool.black]
line-length = 88
target-version = ['py39']
skip-string-normalization = true
include = '\.pyi?$'
extend-exclude = '''
# A regex preceded with ^/ will apply only to files and directories
# in the root of the project.
^/foo.py  # exclude a file named foo.py in the root of the project (in addition to the defaults)
^/.github/workflows/*.yml
'''

[tool.isort]
profile = "black"

[tool.mypy]
python_version = "3.9"
warn_unused_configs = true
exclude = [
    '^file1\.py$',  # TOML literal string (single-quotes, no escaping necessary)
    "^file2\\.py$",  # TOML basic string (double-quotes, backslash and other characters need escaping)
]

[tool.flake8]
max_complexity = 10
max-line-length = 88
show-source = true
benchmark = true

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

## Git Pre-Commit

```bash
pipenv run isort .
```

## References

- [Packaging Python Projects](https://packaging.python.org/en/latest/tutorials/packaging-projects/)
- [PEP 517 - A build-system independent format for source trees](https://peps.python.org/pep-0517/)
- [PEP 518 – Specifying Minimum Build System Requirements for Python Projects](https://peps.python.org/pep-0518/)
- [`flit` Documentation](https://flit.pypa.io/en/latest/)
- [TOML 1.0](https://toml.io/en/v1.0.0)
- [PEP 621 – Storing project metadata in pyproject.toml](https://peps.python.org/pep-0621/)
- [PEP 508 – Dependency specification for Python Software Packages](https://peps.python.org/pep-0508)
- [`pre-commit` Documentation](https://pre-commit.com/)
- [`black` Documentation](https://black.readthedocs.io/en/stable/)
- [`isort` Documentation](https://pycqa.github.io/isort/)
- [`mypy` Documentation](https://mypy.readthedocs.io/en/stable/)
- [`flake8` Documentation](https://flake8.pycqa.org/en/latest/)
- [`pytest` Documentation](https://docs.pytest.org/)
- [`coverage` Documentation](https://coverage.readthedocs.io/)
