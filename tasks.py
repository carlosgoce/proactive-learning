from invoke import run, task


@task
def build():
    run("sphinx-build docs docs/_build")


@task
def autobuild():
    run("sphinx-autobuild docs docs/_build")
