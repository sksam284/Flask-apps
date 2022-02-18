import os
import subprocess


from flask_script import Manager, Server

from app import app
app_settings = os.getenv('FLASK_APP_SETTING', 'app.settings')

manager = Manager(app)

manager.add_command('runserver', Server(threaded=True))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6500)
