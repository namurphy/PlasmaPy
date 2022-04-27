import nox


@nox.session
def tests(session):
    session.install("-r", "requirements/tests.txt")
    session.run("pytest")


@nox.session
def lint(session):
    session.install("-r", "requirements/tests.txt")
    session.run("flake8")
