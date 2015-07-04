from invoke import run, task


@task
def autobuild():
    run("sphinx-autobuild docs docs/_build")
