import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, VARCHAR, TEXT, DATE
from sqlalchemy import  select, and_, MetaData, Table
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy_utils import database_exists
from time import sleep

url = 'postgresql+psycopg2://chillywafflez:ilovekdramas1532@k-drama-tracker-db.cdoxevnwyxjg.us-west-1.rds.amazonaws.com:5432/initial_k_drama_tracker_db'
if not database_exists(url):
    print("bruh")
else:
    print("yippee")

# Session = sessionmaker(bind=engine)
# session = Session()

# metadata = MetaData()
# table = Table('actor', metadata, autoload_with=engine)
# stmt = select(
#     table.columns.first_name,
#     table.columns.last_name
# )
# connection = engine.connect()
# results = connection.execute(stmt).fetchall()
# for result in results:
#     print(result)
# connection.close()
# engine.dispose()



Base = declarative_base()

class Actor(Base):
    __tablename__ = 'actor'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    mdl_id = Column("mdl_id", Integer)
    first_name = Column("first_name", VARCHAR(255))
    last_name = Column("last_name", VARCHAR(255))
    native_name = Column("native_name", VARCHAR(255))
    other_names = Column("other_names", TEXT)
    nationality = Column("nationality", VARCHAR(255))
    gender = Column("gender", VARCHAR(255))
    birthdate = Column("birthdate", DATE)
    age = Column("age", Integer)
    biography = Column("biography", TEXT)
    picture_path = Column("picture_path", TEXT)

    def __init__(self, mdl, first, last, native, other, nationality, gender, birth, age, bio, path):
        self.mdl_id = mdl
        self.first_name = first
        self.last_name = last
        self.native_name = native
        self.other_names = other
        self.nationality = nationality
        self.gender = gender
        self.birthdate = birth
        self.age = age
        self.biography = bio
        self.picture_path = path


engine = create_engine(url)
Session = sessionmaker(bind=engine)
session = Session()

test_actor = Actor(6969, "Justin", "Nguyen", "Justeen", "bruh__hi", "Vietnamese", "Male", "2003-04-28", 20, "blah blah blah", "path_blah_png")
session.add(test_actor)
session.commit()
    
session.close()