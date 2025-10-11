# Setup Python Project

## `pyproject.toml`

```toml
[project.scripts]
<command_name> = "xxx:main"

[project.gui-scripts]
<command_name> = "xxx:main_gui"

[project.entry-points."<group.name>"]
dogelang = "<package>:<name>"
```

## References

- [`flit` Documentation](https://flit.pypa.io/en/latest/)
