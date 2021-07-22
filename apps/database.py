from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session


#SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:password@localhost:3306/db_name" # mysql
#SQLALCHEMY_DATABASE_URL = "postgresql://root:password@localhost:3306/db_name" # postgresql
SQLALCHEMY_DATABASE_URL = "sqlite:///d:/lvup/db/user.db" # mysql

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}) # sqlalchemy engine 생성

# 서버에서 DB에 요청을 보내기 위한 통로 역할
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base() # 이 Base클래스를 상속해 각 데이터베이스 모델 or 클래스 생성

def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()

def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()