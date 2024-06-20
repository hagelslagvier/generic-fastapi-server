### NB.01
If you get the following error:
```text
The virtual environment was not created successfully because ensurepip is not available. On
Debian/Ubuntu systems, you need to install the python3-venv package using the following
command...
```
then run the following command with **explicit minor version** as the following:
```bash
$ sudo apt-get install python3.8-venv
```

### NB.02 

When setting value of `VENV` to `venv_dir` in `Justfile`, also exclude it in `ruff` config section 
in `pyproject.toml` as following:
```text
[tool.ruff]
exclude = ["venv_dir"]
```
For more, see the [link](https://docs.astral.sh/ruff/settings/#exclude).