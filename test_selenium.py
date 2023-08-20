import unittest
import os
from config import basedir
from apps import create_app, db
from selenium import webdriver
from flask_testing import LiveServerTestCase
from apps.models import *
from manage import init
import time
import threading


class SeleniumTestCase(unittest.TestCase):
    client = None

    @classmethod
    def setUpClass(cls):
        # Start Chrome
        # options.add_argument('headless')
        try:
            cls.client = webdriver.Chrome()
        except:
            pass

        # If the browser fails to start, pass the test
        if cls.client:
            # Create application
            cls.app = create_app()
            cls.app.config['TESTING'] = True
            cls.app.config['CSRF_ENABLED'] = False
            cls.app.config['WTF_CSRF_ENABLED'] = False
            cls.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'unittest.db')
            cls.app_context = cls.app.app_context()
            cls.app_context.push()
            db.drop_all()
            db.create_all()
            categories = ['one', 'two', 'three', 'four', 'five', 'Ricardo']
            for category in categories:
                pc = PostCategory(name=category)
                db.session.add(pc)
            db.session.commit()


            # Suppress logging to keep unit test output clean
            import logging
            logger = logging.getLogger('werkzeug')
            logger.setLevel("ERROR")


            # Start the flash service in a thread
            cls.server_thread = threading.Thread(
                target=cls.app.run, kwargs={'debug': 'false',
                                            'use_reloader': False,
                                            'use_debugger': False})
            cls.server_thread.start()

    @classmethod
    def tearDownClass(cls):
        if cls.client:
            # Stop the flask service and browser
            cls.client.quit()
            # cls.server_thread.join()

            # destroy database
            db.drop_all()
            db.session.remove()

            # Remove application context
            cls.app_context.pop()

    def setUp(self):
        if not self.client:
            self.skipTest('没有Web浏览器')

    def tearDown(self):
        pass

    def test_admin_home_page(self):
        # Navigate to the home page
        self.client.get('http://localhost:5000/')
        #register
        self.client.find_element_by_id('navbarDropdown').click()
        self.client.find_element_by_link_text('Register').click()
        time.sleep(2)
        self.client.find_element_by_id('user_name').send_keys('admin')
        self.client.find_element_by_id('nickname').send_keys('admin')
        self.client.find_element_by_id('user_email').send_keys('admin@qq.com')
        self.client.find_element_by_xpath('/html/body/div[2]/div/div/div[2]/form/div[4]/input').send_keys('12345678')
        self.client.find_element_by_id('confirm_pwd').send_keys('12345678')
        time.sleep(2)
        self.client.find_element_by_css_selector('.source-button.btn.btn-primary.btn-xs.mt-2').click()
        time.sleep(2)
        #post
        self.client.get('http://127.0.0.1:5000/post/cate/1/')
        self.client.find_element_by_css_selector('.btn.btn-secondary.h-75.ml-2').click()
        self.client.find_element_by_id('title').send_keys('test')
        self.client.find_element_by_id('body').send_keys('test')
        self.client.find_element_by_id('submit').click()

        #comment
        self.client.find_element_by_css_selector('.form-control.mt-2.report-textarea').send_keys('test comment')
        self.client.find_element_by_id('commentBtn').click()

        #text backend
        self.client.get('http://127.0.0.1:5000/backend/index/')
        self.client.find_element_by_css_selector('button[@title="Add User"]').click()
        time.sleep(2)
        self.client.find_element_by_id('username').send_keys('test')
        self.client.find_element_by_id('nickname').send_keys('test')
        self.client.find_element_by_id('email').send_keys('test@qq.com')
        self.client.find_element_by_id('password').send_keys('1234567')
        self.client.find_element_by_xpath('//*[@id="addUser"]/div[5]/div/button').click()
        time.sleep(10)




if __name__ == '__main__':
    unittest.main()