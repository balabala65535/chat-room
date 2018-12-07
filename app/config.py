import os
from datetime import timedelta


class Config:

    # 数据库链接
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        # "SQLALCHEMY_DATABASE_URI", "mysql+mysqlconnector://root:wolongdata@mysql.test.cdecube.com:3306/infosys?charset=utf8mb4"
        "SQLALCHEMY_DATABASE_URI", "mysql+mysqlconnector://root:123456@127.0.0.1:3306/test?charset=utf8mb4"
        # "SQLALCHEMY_DATABASE_URI", "mysql+mysqlconnector://root:123456@127.0.0.1:3308/infosys?charset=utf8mb4"
        # "SQLALCHEMY_DATABASE_URI", "mysql+mysqlconnector://root:123456@127.0.0.1:3306/infosys_test?charset=utf8mb4"
    )
    SQLALCHEMY_MAX_OVERFLOW = int(
        os.environ.get("SQLALCHEMY_MAX_OVERFLOW", 20))
    SQLALCHEMY_POOL_RECYCLE = int(
        os.environ.get("SQLALCHEMY_POOL_RECYCLE", 60 * 60))
    SQLALCHEMY_POOL_SIZE = int(os.environ.get("SQLALCHEMY_POOL_SIZE", 100))
    REMEMBER_COOKIE_DURATION = timedelta(hours=2)
    PERMANENT_SESSION_LIFETIME = timedelta(hours=2)
    CATCHAT_MESSAGE_PER_PAGE = 1

