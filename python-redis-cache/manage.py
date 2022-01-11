import os
import subprocess


from flask_script import Manager, Server

from app import app
from app import views
app_settings = os.getenv('FLASK_APP_SETTING', 'app.settings')

manager = Manager(app)

manager.add_command('runserver', Server(threaded=True))


@manager.shell
def shell():
    """
    Creates an interactive python shell
    """
    return dict(app=app)


@manager.command
def test():
    app.config.from_object('app.settings')
    subprocess.run('nose2 -s tests', shell=True, check=True)


if __name__ == '__main__':
    manager.run()
