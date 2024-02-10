import uuid
import random
import os


first_names = ("Nick", "Euegene", "Annie", "Mike", "Lip",
              "George", "Bob", "Ilya", "Andrew", "Kostya")
last_names = ("Hush", "Husk", "Stout", "Fask", "Kirk",
             "Dough", "Po", "Shu", "Wealth", "Tolstoy")
users = []
for i in range(0, int(os.environ["MOCK_AMOUNT_USERS"])):
    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    users.append(
        {
            "email": f"{first_name}.{last_name}{i}@example.com",
            "login": f"{first_name}{i}",
            "first_name": first_name,
            "last_name": last_name,
            "id": str(uuid.uuid4())
        }
    )


films = []
titles = ["Star wars", "Max Payne", "Expendables", "John Kek", "Alice in wonderland", "Wolf", "Kicker",
         "Clockwork Orange", "Kalipso", "Pirates of the Carribean", "Mad Max", "War Chronicles",
         "Bionicles", "Lego", "War Thunder", "Lao Zhin"]
genres = ["Comedy", "Action", "Documentary", "Thriller", "Adventure", "Sci-fi", "TV Series", "Biography",
          "Stand UP", "Mockumentary", "Drama"]
for i in range(0, 100):
    films.append({
        "title": f"{random.choice(titles)} {random.randrange(1, 5)}",
        "description": uuid.uuid4(),
        "imdb_rating": str(random.random()*10-0.01)[:3],
        "genre": random.choices(genres, k=random.randrange(1, 3))
    })