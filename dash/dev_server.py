from flask_failsafe import failsafe


@failsafe
def create_app():
    # note that the import is *inside* this function so that we can catch
    # errors that happen at import time
    from app import app
    return app.server


if __name__ == "__main__":
    # app.server is the underlying flask app
    create_app().run(port="8050", debug=True)
