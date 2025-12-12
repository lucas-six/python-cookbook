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
# uv init --python <x.y>

# For example:
uv init -p 3.13
# uv init --python 3.13

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

uv run --env-file .env <python-cmd>  # or UV_ENV_FILE = .env
```

Examples:

```bash
uv run a.py

uv run django-admin startproject a
uv run --env-file .env manage.py runserver

uv run uwsgi a.ini
```

## Deploy a Project

```bash
uv sync [--locked --no-dev]
```

## Update Virtual Environment

```bash
uv venv
```

## Update `uv`

```bash
uv self update
uv self version  # show version
```

## References

- [`uv` Documentation](https://docs.astral.sh/uv/)
- [Python - `venv` module](https://docs.python.org/3/library/venv.html)
- [PEP 405 – Python Virtual Environments](https://peps.python.org/pep-0405/)
- [`uv` Docker Images](https://docs.astral.sh/uv/guides/integration/docker/#available-images)
