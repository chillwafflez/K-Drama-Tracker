from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker
import requests
from db_utils.db_connection import get_engine, get_connection
from db_utils.db_models import Actor


def move_actor_to_db(actor_details, character_details, actor_picture_URL): 
    # Save cover to folder
    cleaned_first_name = actor_details['First Name'].strip().replace(" ", "")
    cleaned_last_name = actor_details['Family Name'].strip().replace(" ", "")
    birth_year = actor_details['Born'].split(',')[1].strip()
    picture_path = "data/actor_covers/" + cleaned_first_name + "__" + cleaned_last_name + "__" + birth_year + "__" + str(actor_details['MDL ID']) + ".jpg"
    with open(picture_path, 'wb') as f:
        response = requests.get(actor_picture_URL)
        f.write(response.content)
    print(f"ACTOR PICTURE PATH: {picture_path}")


    engine = get_engine()
    Session = sessionmaker(bind=engine)
    session = Session()

    # test_actor = Actor(6969, "Justin", "Nguyen", "Justeen", "bruh__hi", "Vietnamese", "Male", "2003-04-28", 20, "blah blah blah", "path_blah_png")
    actor = Actor(actor_details['MDL ID'], actor_details['First Name'], actor_details['Family Name'], actor_details['Native name'], actor_details['Also Known as'], actor_details['Nationality'], actor_details['Gender'], actor_details['Born'], actor_details['Age'], actor_details['Biography'], picture_path)
    session.add(actor)
    session.commit()
    session.close()

# test_actor = Actor(6969, "Justin", "Nguyen", "Justeen", "bruh__hi", "Vietnamese", "Male", "2003-04-28", 20, "blah blah blah", "path_blah_png")
# print(test_actor)
# print("yippee")