# Setup Python Project

## Setup Environment

```bash
uv add --dev pytest coverage[toml] pytest-cov
```

## `pyproject.toml`

```toml
[project.optional-dependencies]
test = [
    "pytest",
    "coverage",
    "pytest-cov",
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

## References

- [`flit` Documentation](https://flit.pypa.io/en/latest/)
- [`pytest` Documentation](https://docs.pytest.org/)
- [`coverage` Documentation](https://coverage.readthedocs.io/)
