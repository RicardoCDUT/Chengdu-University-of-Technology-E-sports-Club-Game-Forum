import os
basedir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig(object):

    BBS_PER_PAGE = 20
    BBS_PER_PAGE_SOCIAL = 40
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    DATABASE_USER='flask_bbs'
    DATABASE_PWD='flask_bbs'
    DATABASE_HOST='127.0.0.1'
    DATABASE_PORT=3306
    DATABASE_DB='flask_bbs'
    SECRET_KEY='dev'



    BBS_UPLOAD_PATH = os.path.join(basedir, 'apps/static/uploads')
    AVATARS_SAVE_PATH = BBS_UPLOAD_PATH + '/avatars/'

    # CKEditor configure
    CKEDITOR_SERVE_LOCAL = True
    CKEDITOR_ENABLE_CODESNIPPET = True
    CKEDITOR_HEIGHT = 400
    CKEDITOR_FILE_UPLOADER = 'global.image_upload'
    CKEDITOR_LANGUAGE='en'

    # whooshee config
    WHOOSHEE_MIN_STRING_LEN = 1


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}/{}?charset=utf8mb4'.format(BaseConfig.DATABASE_USER,
                                                                                    BaseConfig.DATABASE_PWD,
                                                                                    BaseConfig.DATABASE_HOST,
                                                                                    BaseConfig.DATABASE_DB)


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}/{}?charset=utf8mb4'.format(BaseConfig.DATABASE_USER,
                                                                                    BaseConfig.DATABASE_PWD,
                                                                                    BaseConfig.DATABASE_HOST,
                                                                                    BaseConfig.DATABASE_DB)
