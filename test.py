import unittest
import os
from config import basedir
from apps import create_app, db

from apps.models import *
import re

def get_csrf(html):
    pattern = re.compile('name="csrf_token" type="hidden" value="(.*?)"')
    return pattern.findall(html)[0]

class TestCase(unittest.TestCase):
    def setUp(self):
        app=create_app()
        app.app_context().push()
        app.config['TESTING'] = True
        app.config['CSRF_ENABLED'] = False
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_comment(self):
        u = User(username = 'john',nickname='john', email = 'john@example.com',password='123')
        db.session.add(u)
        db.session.commit()
        cate=PostCategory(name='one')
        db.session.add(cate)
        db.session.commit()
        self.app.post('/auth/login/', data=dict(usr_email='john',password='123'), follow_redirects=True)
        payload=dict(title='test',body='test',category=1)
        # print(payload)
        self.app.post('/post/new/', data=payload, follow_redirects=True)

        #register a new user
        u2 = User(username = 'john2',nickname='john2', email = 'john2@example.com',password='123')
        db.session.add(u2)
        db.session.commit()
        self.app.post('/auth/login/', data=dict(usr_email='john2',password='123'), follow_redirects=True)
        r2=self.app.post('/post/post-comment/', data=dict(postId=1,commentContent='this is a test comment'), follow_redirects=True)
        if r2.json['success']=='ok':
            print('test comment -> success')
        else:
            print('test comment -> fail')
    
    

    
    def test_create_post(self):
        u = User(username = 'john',nickname='john', email = 'john@example.com',password='123')
        db.session.add(u)
        db.session.commit()
        cate=PostCategory(name='one')
        db.session.add(cate)
        db.session.commit()
        self.app.post('/auth/login/', data=dict(usr_email='john',password='123'), follow_redirects=True)
        payload=dict(title='test',body='test',category=1)
        # print(payload)
        r2 = self.app.post('/post/new/', data=payload, follow_redirects=True)
        if 'test' in r2.data.decode('utf-8'):
            print('test create post -> success')
        else:
            print('test create post -> fail')
     
    def test_login(self):
        u = User(username = 'john',nickname='john', email = 'john@example.com',password='123')
        db.session.add(u)
        db.session.commit()
        response = self.app.post('/auth/login/', data=dict(usr_email='john',password='123'), follow_redirects=True)
        if 'Online' in response.data.decode('utf-8'):
            print('test login -> success')
        else:
            print('test login -> fail')
    
 


    def test_register(self):
        response = self.app.post('/auth/register/', data=dict(user_name='john',nickname='john',password='123',confirm_pwd='123',user_email='jhon@example.com'), follow_redirects=True)
        if 'Online' in response.data.decode('utf-8'):
            print('test register -> success')
        else:
            print('test register -> fail')
    
    def test_get_post_admin(self):
        u = User(username = 'john',nickname='john', email = 'john@example.com',password='123')
        db.session.add(u)
        db.session.commit()
        cate=PostCategory(name='one')
        db.session.add(cate)
        db.session.commit()
        self.app.post('/auth/login/', data=dict(usr_email='john',password='123'), follow_redirects=True)
        payload=dict(title='test',body='test',category=1)
        # print(payload)
        r2 = self.app.post('/post/new/', data=payload, follow_redirects=True)
        r3 = self.app.post('/backend/claims', follow_redirects=True)
        if r3.json['count']==1:
            print('test get post admin -> success')
        else:
            print('test get post admin -> fail')
        
        r4=self.app.post('/backend/del_claim', data=dict(id=1), follow_redirects=True)
        if r4.json['info']=='Delete claim Success!':
            print('test del claim -> success')
        else:
            print('test del claim -> fail')
    
    



if __name__ == '__main__':
    unittest.main()