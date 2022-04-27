import nox

python_versions = ("3.8", "3.9", "3.10")


@nox.session(python=python_versions, reuse_venv=True)
def tests(session):
    session.install("-r", "requirements/tests.txt")
    session.run("pytest")


@nox.session
def linters(session):
    session.install("-r", "requirements/tests.txt")
    session.run("flake8", "--bug-report")
    flake8_options = ["--count", "--show-source", "--statistics"]
    session.run("flake8", "plasmapy", *flake8_options)


@nox.session
def build_docs(session):
    session.install("-r", "requirements/docs.txt")
    session.run(
        "sphinx-build",
        "docs",
        "docs/_build/html",
        "-W",
        "--keep-going",
        "-b",
        "html",
        *session.posargs,
    )


@nox.session
def codespell(session):
    session.install("codespell")
    session.run("codespell", ".")
