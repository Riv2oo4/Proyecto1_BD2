import pandas as pd
import json

def clean_and_transform_csv(input_file, output_file):
    # Cargar el archivo CSV
    df = pd.read_csv(input_file)
    
    # Seleccionar solo las columnas necesarias
    df = df[['original_title', 'original_language', 'popularity', 'spoken_languages', 'genres', 'production_companies', 'production_countries']]
    
    # Función para convertir JSON-like en listas
    def parse_json_column(column):
        def safe_parse(value):
            try:
                return [item['name'] for item in json.loads(value)] if pd.notna(value) and value.startswith('[') else []
            except json.JSONDecodeError:
                return []
        return column.apply(safe_parse)
    
    df['genres'] = parse_json_column(df['genres'])
    df['production_companies'] = parse_json_column(df['production_companies'])
    df['production_countries'] = parse_json_column(df['production_countries'])
    df['spoken_languages'] = parse_json_column(df['spoken_languages'])
    
    # Guardar el archivo limpio
    df.to_csv(output_file, index=False)
    print(f"Archivo procesado guardado en {output_file}")

# Uso
input_csv = "tmdb_5000_movies.csv"  # Cambia esto por tu archivo real
output_csv = "cleaned_movies.csv"
clean_and_transform_csv(input_csv, output_csv)