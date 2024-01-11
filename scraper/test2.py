# import re
import csv

# bruh = "TwinklingWatermelon's_2023_739603"

# yuh = re.sub(r'[^\w.-]', '', bruh)
# print(yuh)
# print(bruh)

def main():
    with open ('data\completed_SK_extra_info.csv', 'r') as csvfile:
       reader = csv.reader (csvfile, delimiter=',')
       next(reader)     # skip first row which are just column headers
       for row in reader: # loop over the rows
        drama_title = row[0]
        year = row[1]
        mdl_id = row[2]
        network_string = row[3]
        genre_string = row[4]
        tag_string = row[5]
        print(tag_string)

main()