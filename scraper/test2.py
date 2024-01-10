import pandas as pd
import csv

# title = "Moving"
# title_with_year = "Moving (2023)"
# mld_id = 25560
# genres = "Action,Thriller,Mystery,Supernatural"
# tags = "Graphic Violence,Supernatural Power,Student Female Lead,Student Male Lead,Agent Female Lead,Agent Male Lead,Family Relationship,Past And Present,Multiple Mains,High School"

title = "Yeonhwa Palace"
title_with_year = "Yeonhwa Palace (1967)"
mld_id = 710963
networks = "Netflix,tvN"
genres = "Historical,Melodrama"
tags = "Palace Setting,Prince Male Lead,Historical Fiction,Royalty,Joseon Dynasty"

# data = {'title': title,
#         'title_year': title_with_year,
#         'mdl_id': mld_id,
#         'genres': genres,
#         'tags': tags}
# df = pd.DataFrame(data, index=[0])

# print(df)
# with open("./scraped_data/completed_SK_genres_tags.csv", 'a') as f:
#     df.to_csv(f, index=False, header=False, lineterminator='\n')

# # Using csv module
with open("./data/completed_SK_genres_tags.csv", mode='a', newline='') as f:
    writer = csv.writer(f)
    writer.writerow([title, title_with_year, mld_id, networks, genres, tags])


    
# df.to_csv("./scraped_data/completed_SK_genres_tags.csv", mode='a', index=False, header=False)


# df = pd.read_csv("./scraped_data/completed_SK_genres_tags.csv", usecols=['title'])
# print(df)