# Developer Guide

Any contributions to this project are very welcome!
If you have an idea that you would like to implement,
please raise an issue and mention that you would like to contribute.

## Pull requests

To create a pull request,
fork the repository.
Then create a branch with a descriptive name.

You are welcome to open a pull request early on.
If you do so,
please open a draft pull request.

We use [`pre-commit`](https://pre-commit.com/)
in order to ensure formatting before committing to `git`.
using a pre-commit hook.

## Documentation

Better documentation is always welcome!

We use [`mkdocs`](https://www.mkdocs.org/) to generate the documentation.
To build or serve the documentation locally,
you will need to install `mkdocs` and the `mkdocs-mermaid2-plugin`.
If you are using `rye` for python management (see [below](#python-development)),
these dependencies will be automatically installed.
In this case you can run `mkdocs` with

```bash
rye run docs
```

Please consult the `mkdocs` documentation for further details
on installation into other environments.

## Python development

### Setup

We use [`rye`](https://rye-up.com/) to manage the python environment.
This guide assumes that you have `rye` installed and set up.
However, we add info boxes for other environments where necessary.

!!! note
    The reason for using `rye` is that it allows us to
    set up the project as a workspace.
    The workspace itself has no python package,
    however,
    it consists of the `controller_cli` package
    and the `controller` GUI.

!!! info
    If you are not using `rye`,
    you will need to install development dependencies manually.
    See the `pyproject.toml` file for details,
    especially the section `[tool.rye.dev-dependencies]`.

In addition to `rye`,
you should have `pre-commit` installed and available in your path.
With `rye`, this can easily be done by running

```bash
rye install pre-commit
```



### Linting and formatting

We use [`ruff`](https://docs.astral.sh/ruff/) to lint and format the code.
Please make sure that code is properly linted before committing.
You can run the linter with

```bash
rye run lint
```

!!! tip
    You can also run `rye run lint --fix` to automatically fix some issues.

!!! info
    If you are not using `rye`,
    you can run `ruff` directly.
    However, you will need to install `ruff` in your environment.
    See the `ruff` documentation for details.

### Testing

!!! warning
    Currently, only the `controller_cli` module is tested.
    The `controller` (GUI) module is not tested yet.

We use [`pytest`](https://docs.pytest.org/) for testing.
All tests are located in the `tests` folder.
You can run the tests with

```bash
rye run test
```

!!! info
    If you are not using `rye`,
    you can run `pytest` directly
    (e.g., `pytest .` in the `controller_cli` folder).

### GUI development

#### Imports and GUI toolkit

As a default dependency,
we add `PyQt6` to the `pyproject.toml` file.
However, you can also use `PySide` if you like.
All imports in the code enable both
by using [`qtpy`](https://pypi.org/project/QtPy/).

#### Packaging

We use [`fbs`](https://build-system.fman.io/) to package the GUI.
If you want to package the GUI,
you will need an `fbs-pro` license.
However,
packaging is not necessary for development.

The reason for using `fbs` is that it allows us to
package the GUI for standalone execution
on air-gapped systems.
Laboratory computers are often not connected to the internet,
therefore this is a requirement for us.

#### Structure

Unfortunately,
using `fbs` requires a specific structure of the project.
The sources for the GUI are located in the `src/main/python` folder.

#### Running the GUI

There are various ways that you can use to run the GUI.
The easiest way is to run

```bash
rye run gui
```

However,
if you are using an IDE,
you can also run the `main.py` file directly.

At the bottom of the `main.py` file,
you can see that there are two actual ways to run the GUI:
with `fbs` and without `fbs` installed.
If you use either of the described methods to start the GUI,
the `gui_start` method in the `main.py` file will be called.
This method automatically detects
whether `fbs` is installed or not.

## Firmware

The firmware is written in Arduino C++.
Please see the [firmware documentation](firmware.md) for details
on installation.

## Hardware

If you would like to contribute hardware designs,
please get in touch with us by raising an issue.
