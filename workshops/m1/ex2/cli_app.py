import argparse

def append_film(film_name, stars):
    with open("films.csv", "a") as file:
        file.write(f'{film_name},{stars}\n')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('--film-name')
    parser.add_argument( '--stars')

    args = parser.parse_args()

    film_name = args.film_name
    stars = args.stars

# print(film_name, stars)