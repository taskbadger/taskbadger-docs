from invoke import task


@task
def serve(c):
    c.run("mkdocs serve -a localhost:8080")
