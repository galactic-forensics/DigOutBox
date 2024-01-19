"""Configuration file for testing the package with ``nox``."""

import tomllib

import nox

# get dev dependencies from rye config in pyproject.toml
with open("pyproject.toml", "rb") as f:
    toml_data = tomllib.load(f)
dev_req = toml_data["tool"]["rye"]["dev-dependencies"]

nox.options.sessions = ["lint", "tests"]

package = "controller_cli"
locations = ["src/controller_cli"]

python_default = "3.12"
python_suite = ["3.12", "3.11", "3.10", "3.9", "3.8"]


@nox.session(python=python_default)
def lint(session):
    """Lint project using ``flake8``."""
    args = session.posargs or locations
    session.install(*dev_req)
    session.install(".")
    session.run("flake8", *args)


@nox.session(python=python_suite)
def tests(session):
    """Test the project using ``pytest``."""
    session.install(*dev_req)
    session.install(".")
    session.run("pytest")


@nox.session(python=python_default)
def safety(session):
    """Safety check for all dependencies."""
    session.install("safety", ".")
    session.run(
        "safety",
        "check",
        "--full-report",
    )
