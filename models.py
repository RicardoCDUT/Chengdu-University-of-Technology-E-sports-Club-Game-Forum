import datetime
from . import db
from flask_avatars import Identicon
from flask_login import UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from bleach import clean, linkify
from bs4 import BeautifulSoup
from markdown import markdown
from markdown import extensions
from markdown.treeprocessors import Treeprocessor

class md_ext_self(Treeprocessor):
    def run(self, root):
        for child in root.iter():
            if child.tag == 'table':
                child.set("class", "table table-bordered table-hover")
            elif child.tag == 'img':
                child.set("class", "img-fluid d-block img-pd10")
            elif child.tag == 'blockquote':
                child.set('class', 'blockquote-comment')
            elif child.tag == 'p':
                child.set('class', 'mt-0 mb-0 p-break')
            elif child.tag == 'pre':
                child.set('class', 'mb-0')
            elif child.tag == 'h1':
                child.set('class', 'comment-h1')
            elif child.tag == 'h2':
                child.set('class', 'comment-h2')
            elif child.tag == 'h3':
                child.set('class', 'comment-h3')
            elif child.tag in ['h4', 'h5', 'h6']:
                child.set('class', 'comment-h4')
        return root


# noinspection PyAttributeOutsideInit
class md_ext(extensions.Extension):
    def extendMarkdown(self, md):
        md.registerExtension(self)
        self.processor = md_ext_self()
        self.processor.md = md
        self.processor.config = self.getConfigs()
        md.treeprocessors.add('mystyle', self.processor, '_end')

def get_text_plain(html_text):
    bs = BeautifulSoup(html_text, 'html.parser')
    return bs.get_text()


# noinspection PyTypeChecker
def to_html(raw):
    allowed_tags = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a', 'abbr', 'b', 'br', 'blockquote', 'code', 'del', 'div',
                    'em', 'img', 'p', 'pre', 'strong', 'span', 'ul', 'li', 'ol']
    allowed_attributes = ['src', 'title', 'alt', 'href', 'class']
    html = markdown(raw, output_format='html',
                    extensions=['markdown.extensions.fenced_code',
                                'markdown.extensions.codehilite',
                                'markdown.extensions.tables', md_ext()])
    clean_html = clean(html, tags=allowed_tags, attributes=allowed_attributes)
    return linkify(clean_html)



class Follow(db.Model):
    #Users pay attention to each other
    __tablename__ = 'follow'

    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    follower_id = db.Column(db.INTEGER, db.ForeignKey('user.id'))
    followed_id = db.Column(db.INTEGER, db.ForeignKey('user.id'))
    #PK,FK

    # People following users
    follower = db.relationship('User', foreign_keys=[follower_id], back_populates='following', lazy='joined')
    # The person the user is following
    followed = db.relationship('User', foreign_keys=[followed_id], back_populates='followers', lazy='joined')

class User(db.Model, UserMixin):
    __tablename__ = 'user'
#User information table
    id = db.Column(db.INTEGER, primary_key=True, nullable=False, index=True, autoincrement=True)
    username = db.Column(db.String(40), nullable=False, index=True, unique=True, comment='user name')
    nickname = db.Column(db.String(40), nullable=False, unique=True, comment='user nick name')
    password_hash = db.Column(db.String(256), comment='user password')
    email = db.Column(db.String(128), unique=True, nullable=False, comment='user register email')
    avatar = db.Column(db.String(100), nullable=False, comment='user avatar')
    avatar_raw = db.Column(db.String(100), comment='use avatar raw file')
    create_time = db.Column(db.DATETIME, default=datetime.datetime.now)

#Data associated with other tables
    post = db.relationship('Post', back_populates='user', cascade='all')
    collect = db.relationship('Collect', back_populates='user', cascade='all')
    comments = db.relationship('Comments', back_populates='author', cascade='all')
    following = db.relationship('Follow', foreign_keys=[Follow.follower_id], back_populates='follower',
                                lazy='dynamic', cascade='all')
    followers = db.relationship('Follow', foreign_keys=[Follow.followed_id], back_populates='followed',
                                lazy='dynamic', cascade='all')


    receive_notify = db.relationship('Notification', back_populates='receive_user', cascade='all')

    def __init__(self,**kwargs):
        super(User, self).__init__(**kwargs)
        if self.avatar is None:
            icon = Identicon()
            files = icon.generate(self.username)
            self.avatar = '/static/uploads/avatars/' + files[2]

    # Encrypt and save the password
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

#Set password
    def check_password(self, pwd):
        return check_password_hash(self.password_hash, pwd)

#Get permission
    def is_following(self, user):
        if user.id is None:
            return False
        return self.following.filter_by(followed_id=user.id).first() is not None
#Does he pay attention to other users
    def unfollow(self, user):
        follow = self.following.filter_by(followed_id=user.id).first()
        if follow:
            db.session.delete(follow)
            db.session.commit()
#Cancel paying attention to other users
    def follow(self, user):
        if not self.is_following(user):
            follow = Follow(follower=self, followed=user)
            db.session.add(follow)
            db.session.commit()
#Focus on users

class PostCategory(db.Model):
    __tablename__ = 'postcate'
#Classification of topics
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    name = db.Column(db.String(40), nullable=False)
    create_time = db.Column(db.Date, default=datetime.date.today)

    post = db.relationship('Post', back_populates='cats', cascade='all')


class Post(db.Model):
    __tablename__ = 'post'
    #Posting table

    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True, index=True)
    title = db.Column(db.String(100), index=True, nullable=False)
    content = db.Column(db.TEXT, nullable=False)
    textplain = db.Column(db.TEXT, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.datetime.now)
    read_times = db.Column(db.INTEGER, default=0)
    likes = db.Column(db.INTEGER, default=0, comment='like post persons')
    unlikes = db.Column(db.INTEGER, default=0, comment='unlike post persons')
    collects = db.Column(db.INTEGER, default=0, comment='collect post persons')
#Corresponding to which category, the ID of the sender
    cate_id = db.Column(db.INTEGER, db.ForeignKey('postcate.id'))
    author_id = db.Column(db.INTEGER, db.ForeignKey('user.id'))

    cats = db.relationship('PostCategory', back_populates='post')
    user = db.relationship('User', back_populates='post')
    collect = db.relationship('Collect', back_populates='post', cascade='all')
    comments = db.relationship('Comments', back_populates='post', cascade='all')

    def can_delete(self):
        return current_user.id == self.author_id


class Comments(db.Model):
    #Table of comments
    __tablename__ = 'comments'
#ID of the comment
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    body = db.Column(db.Text)
    timestamps = db.Column(db.DATETIME, default=datetime.datetime.now)
#Reply ID
    replied_id = db.Column(db.INTEGER, db.ForeignKey('comments.id'))
    author_id = db.Column(db.INTEGER, db.ForeignKey('user.id'))
    post_id = db.Column(db.INTEGER, db.ForeignKey('post.id'))
    likes = db.Column(db.INTEGER, default=0, comment='like post persons')
    unlikes = db.Column(db.INTEGER, default=0, comment='unlike post persons')
#Which article does it correspond to
    post = db.relationship('Post', back_populates='comments')
    author = db.relationship('User', back_populates='comments')
    replies = db.relationship('Comments', back_populates='replied', cascade='all')
    replied = db.relationship('Comments', back_populates='replies', remote_side=[id])

    def can_delete(self):
        return self.author_id == current_user.id


class Collect(db.Model):
    #Collection table
    __tablename__ = 'collect'

    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    user_id = db.Column(db.INTEGER, db.ForeignKey('user.id'))
    post_id = db.Column(db.INTEGER, db.ForeignKey('post.id'))
    timestamps = db.Column(db.DateTime, default=datetime.datetime.now)

    user = db.relationship('User', back_populates='collect', lazy='joined')
    post = db.relationship('Post', back_populates='collect', lazy='joined')



class Notification(db.Model):
    __tablename__ = 'notification'
    #Table of notification messages
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    type = db.Column(db.INTEGER, default=0, comment='notification type 1 post')
    target_id = db.Column(db.INTEGER)
    target_name = db.Column(db.String(200))
    send_user = db.Column(db.String(40))
    receive_id = db.Column(db.INTEGER, db.ForeignKey('user.id'))
    msg = db.Column(db.String(400))
    read = db.Column(db.INTEGER, default=0, comment='is read? 0 no 1 yes')
    timestamp = db.Column(db.DateTime, default=datetime.datetime.now)
    receive_user = db.relationship('User', back_populates='receive_notify')

#Statistical table
class Statistic(db.Model):
    __tablename__ = 'statistic'
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    times = db.Column(db.INTEGER, default=0)
    day = db.Column(db.Date, default=datetime.date.today)
    _type=db.Column(db.String(20), default='visit')


