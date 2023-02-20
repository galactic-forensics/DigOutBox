"""Configuration file for testing the package with ``nox``."""

import nox

nox.options.sessions = ["lint", "tests"]

package = "controller_cli"
locations = ["controller_cli"]

python_default = "3.10"
python_suite = ["3.11", "3.10", "3.9", "3.8"]


@nox.session(python=python_default)
def lint(session):
    """Lint project using ``flake8``."""
    args = session.posargs or locations
    session.install(".[dev]")
    session.run("flake8", *args)


@nox.session(python=python_suite)
def tests(session):
    """Test the project using ``pytest``."""
    session.install(".[test]")
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
