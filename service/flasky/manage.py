import os
from app import create_app, db
from flask_script import Manager, Shell, Command

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)


def make_shell_context():
    # manager.add_command("shell", Shell(make_context=make_shell_context))
    # manager.add_command('db', MigrateCommand)
    return dict(app=app, db=db)


if __name__ == '__main__':
    manager.run()
