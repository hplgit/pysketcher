import glob
import shutil
import tempfile

import nox
from nox.sessions import Session
import nox_poetry.patch  # noqa: F401

nox.options.sessions = "lint", "safety", "tests", "examples"
nox.options.reuse_existing_virtualenvs = True
locations = "pysketcher", "tests", "examples", "docs", "noxfile.py"

main_version = ["3.8"]
supported_versions = ["3.8", "3.9"]


@nox.session(python=main_version)
def lint(session: Session) -> None:
    args = session.posargs or locations
    session.install(
        "darglint",
        "flake8",
        "flake8-bandit",
        "flake8-black",
        "flake8-bugbear",
        "flake8-docstrings",
        "flake8-import-order",
    )
    session.run("flake8", *args)


@nox.session(python=supported_versions)
def tests(session: Session) -> None:
    session.install(".")
    session.install("pytest", "coverage[toml]", "hypothesis", "pytest-cov")
    session.run("poetry", "install", external=True)
    session.run("pytest", "--cov")


@nox.session(python=supported_versions)
def examples(session: Session) -> None:
    session.install(".")
    session.install("pytest", "coverage[toml]", "hypothesis", "pytest-cov")
    session.run("poetry", "install", external=True)
    session.run(
        "pytest",
        "--cov",
        "--cov-append",
        "-o",
        "testpaths=examples",
        "-o",
        "python_files=*.py",
        "-o",
        "python_functions=main",
    )


@nox.session(python=main_version)
def coverage(session: Session) -> None:
    """Upload coverage data."""
    session.install("coverage[toml]", "codecov")
    session.run("coverage", "xml", "--fail-under=0")
    session.run("codecov", *session.posargs)


@nox.session(python=main_version)
def black(session: Session) -> None:
    args = session.posargs or locations
    session.install("black", "blackdoc")
    session.run("black", *args)
    session.run("blackdoc", *args)


@nox.session(python=main_version)
def safety(session: Session) -> None:
    with tempfile.NamedTemporaryFile() as requirements:
        session.run(
            "poetry",
            "export",
            "--dev",
            "--format=requirements.txt",
            "--without-hashes",
            f"--output={requirements.name}",
            external=True,
        )
        session.install("safety")
        session.run("safety", "check", f"--file={requirements.name}", "--full-report")


@nox.session(python=main_version)
def docs(session: Session) -> None:
    """Build the documentation."""
    session.install(".")
    session.install("sphinx", "sphinx-autodoc-typehints", "sphinx-rtd-theme")
    session.install("pytest", "hypothesis")
    session.run("pytest", "pysketcher")  # generate the images by running the docstrings
    for file in glob.glob("./pysketcher/images/*.png"):
        print(f"{file}")
        shutil.copy(file, "./docs/images")
    session.run("sphinx-build", "docs", "docs/_build")
