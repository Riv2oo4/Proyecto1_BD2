import pandas as pd

movies_path = r"DATA\tmdb_5000_movies.csv"
credits_path = r"DATA\tmdb_5000_credits.csv"
movies_df = pd.read_csv(movies_path)
credits_df = pd.read_csv(credits_path)
print("Peliculas:")
print(movies_df.head())

print("\Creditos:")
print(credits_df.head())

