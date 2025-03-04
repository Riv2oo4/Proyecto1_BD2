import pandas as pd

# Rutas de los archivos CSV
movies_path = r"DATA\critic_reviews.csv"
users_path = r"DATA\movies.csv"
reviews_path = r"DATA\critic_reviews.csv"

# Cargar los CSV en DataFrames
movies_df = pd.read_csv(movies_path)
users_df = pd.read_csv(users_path)
reviews_df = pd.read_csv(reviews_path)

# Mostrar las primeras filas de cada archivo
print("Películas:")
print(movies_df.head())

print("\nUsuarios:")
print(users_df.head())

print("\nReseñas:")
print(reviews_df.head())
