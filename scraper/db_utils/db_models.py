from sqlalchemy import ForeignKey, Column, String, Integer, VARCHAR, TEXT, DATE, NUMERIC, BOOLEAN
from sqlalchemy import MetaData, Table
from sqlalchemy.orm import declarative_base

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
    
    def __repr__(self):
        return f"HIII {self.first_name}"

class Drama(Base):
    __tablename__ = 'drama'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    mdl_id = Column("mdl_id", Integer)
    title = Column("title", VARCHAR(255))
    native_title = Column("native_title", VARCHAR(255))
    other_names = Column("other_names", TEXT)
    rating = Column("rating", NUMERIC)
    MDL_rating = Column("MDL_rating", NUMERIC)
    synopsis = Column("synopsis", TEXT)
    episode_count = Column("episode_count", Integer)
    duration = Column("duration", Integer)
    content_rating = Column("content_rating", VARCHAR(255))
    country = Column("country", VARCHAR(255))
    air_date = Column("air_date", VARCHAR(255))
    air_year = Column("air_year", Integer)
    airing = Column("airing", BOOLEAN)
    cover_path = Column("cover_path", VARCHAR(255))

    def __init__(self, mdl, title, native_title, other_names, rating, MDL_rating, synopsis, episode_count, duration, content_rating, country, air_date, air_year, airing, cover_path):
        self.mdl_id = mdl
        self.title = title
        self.native_title = native_title
        self.other_names = other_names
        self.rating = rating
        self.MDL_rating = MDL_rating
        self.synopsis = synopsis
        self.episode_count = episode_count
        self.duration = duration
        self.content_rating = content_rating
        self.country = country
        self.air_date = air_date
        self.air_year = air_year
        self.airing = airing
        self.cover_path = cover_path
        
class Character(Base):
    __tablename__ = 'character'

    actor_id = Column("actor_id", Integer, ForeignKey("actor.id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    drama_id = Column("drama_id", Integer, ForeignKey("drama.id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    character_name = Column("character_name", VARCHAR(255))
    actor_role = Column("actor_role", VARCHAR(255))

    def __init__(self, actor_id, drama_id, character_name, actor_role):
        self.actor_id = actor_id
        self.drama_id = drama_id
        self.character_name = character_name
        self.actor_role = actor_role

# def main():
#     engine = get_engine()
#     Session = sessionmaker(bind=engine)
#     session = Session()

#     # test_actor = Actor(6969, "Justin", "Nguyen", "Justeen", "bruh__hi", "Vietnamese", "Male", "2003-04-28", 20, "blah blah blah", "path_blah_png")
#     character = Character(1, 3, "Shrek", "Main Role")
#     session.add(character)
#     session.commit()
#     session.close()
#     engine.dispose()

# main()