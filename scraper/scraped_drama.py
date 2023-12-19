from typing import List

class Drama:
    def __init__(self, data_id: int, 
                       title: str, 
                       country: str, 
                       native_title: str, 
                       synopsis: str, 
                       rating: int, 
                       other_names: List[str], 
                       episode_count: int, 
                       air_date: str, 
                       genres: List[str], 
                       tags: List[str], 
                       original_networks: List[str], 
                       content_rating: str):
        self.data_id = data_id
        self.title = title
        self.country = country
        self.native_title = native_title
        self.synopsis = synopsis
        self.rating = rating
        self.other_names = other_names
        self.episode_count = episode_count
        self.air_date = air_date
        self.genres = genres
        self.tags = tags
        self.original_networks = original_networks
        self.content_rating = content_rating

class Actor:
    def __init__(self, first_name, family_name, native_name, nationality, gender, birth_date, age, biography):
        self.first_name = first_name,
        self.family_name = family_name
        self.native_name = native_name,
        self.nationality = nationality
        self.gender = gender,
        self.birth_date = birth_date
        self.age = age
        self.biography = biography



    
