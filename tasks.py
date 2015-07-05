from invoke import run, task


@task
def build():
    run("sphinx-build docs docs/_build")


@task
def autobuild():
    run("open http://127.0.0.1:8000")
    run("sphinx-autobuild docs docs/_build")
