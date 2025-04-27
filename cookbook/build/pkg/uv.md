# `uv`

An extremely fast Python package and project manager, written in *Rust*.

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

or

```bash
pip install uv
```

## Create Project and Virtual Environment

```bash
cd <project-dir>
uv init -p <x.y>

# For example:
uv init -p 3.12

# or default version:
uv init
```

## Package Indexes (Mirror)

```toml
# pyproject.toml

[[tool.uv.index]]
url = "https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple"
default = true
```

## Install Packages/Dependencies

```bash
uv add <pkg ...>
uv add --dev <pkg ...>  # for development
```

## Uninstall Packages/Dependencies

```bash
uv remove <pkg ...>
uv remove --dev <pkg ...>  # for development
```

## Run

```bash
uv run <python-cmd>
```

Examples:

```bash
uv run python a.py

uv run django-admin startproject a
uv run python manage.py runserver

uv run uwsgi a.ini
```

## Deploy a Project

```bash
uv sync
```

## References

- [`uv` Documentation](https://docs.astral.sh/uv/)
- [Python - `venv` module](https://docs.python.org/3/library/venv.html)
- [PEP 405 – Python Virtual Environments](https://peps.python.org/pep-0405/)
