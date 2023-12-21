import pandas as pd

def move_to_csv():
    data = [
        {'title': "Moving", 'ep_count': 14, 'genres': ['penis', 'cock', 'ball'], 'airing': True},
        {'title': "Squid Game", 'ep_count': 8, 'genres': ['horror', 'thriller'], 'airing': False},
        {'title': "Itaewon Class", 'ep_count': 10, 'genres': ['bruh', 'apple', 'banana'], 'airing': True}
    ]

    df = pd.DataFrame(data)

    print(df)

    df.to_csv("scraped_data/test.csv", index=False)

def get_from_csv():
    df = pd.read_csv("scraped_data/test.csv")
    bruh = df.iloc[1]
    print(type(bruh['airing']))

get_from_csv()