from apps import create_app, db
from apps.models import *
from flask_migrate import Migrate
import sys
import re

app = create_app(config_name='production')
app.jinja_env.globals['sitename']='FlaskBBS'

migrate = Migrate(app, db)


def init(create_su=True):
    app.app_context().push()
    db.drop_all()
    db.create_all()
    init_cate()
    db.session.commit()
    print('Database initialization completed!')
    if create_su:
        create_superuser()
    print('Project initialization completed!')


def create_superuser():
    reg = '^[a-zA-Z0-9_]*$'
    inp = True
    while inp:
        username = input('Please enter the super administrator user name (not Chinese):')
        nickname = input('Please enter the super administrator nickname:')
        pwd = input('Please enter the super administrator password (greater than 8 digits):')
        if re.match(reg, username) or len(pwd) > 8:
            inp = False

    u = User(username=username, nickname=nickname,password=pwd, email='admin@gmail.com')
    db.session.add(u)
    db.session.commit()
    print('Super administrator added successfully!')


def init_cate():
    categories = ['Life', 'Game', 'Animation', 'Free', 'Text', 'Ricardo']
    for category in categories:
        pc = PostCategory(name=category)
        db.session.add(pc)
    db.session.commit()



if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'init':
        init()
    else:
        app.run(debug=True)