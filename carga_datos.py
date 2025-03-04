from neo4j import GraphDatabase
import pandas as pd

class Neo4jConnection:
    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))
    
    def close(self):
        self._driver.close()
    
    def run_query(self, query, parameters=None):
        with self._driver.session() as session:
            return session.run(query, parameters)

class MovieDatabase:
    def __init__(self, db_connection):
        self.db = db_connection
    
    def create_movie(self, title, language, popularity):
        query = """
        MERGE (m:Movie {title: $title})
        ON CREATE SET m.language = $language, m.popularity = $popularity
        RETURN m
        """
        self.db.run_query(query, {"title": title, "language": language, "popularity": popularity})
    
    def create_genre(self, genre_name):
        query = "MERGE (g:Genre {name: $genre_name}) RETURN g"
        self.db.run_query(query, {"genre_name": genre_name})
    
    def create_production_company(self, company_name):
        query = "MERGE (c:ProductionCompany {name: $company_name}) RETURN c"
        self.db.run_query(query, {"company_name": company_name})
    
    def create_country(self, country_name):
        query = "MERGE (p:ProductionCountry {name: $country_name}) RETURN p"
        self.db.run_query(query, {"country_name": country_name})
    
    def create_director(self, director_name):
        query = "MERGE (d:Director {name: $director_name}) RETURN d"
        self.db.run_query(query, {"director_name": director_name})
    
    def create_actor(self, actor_name):
        query = "MERGE (a:Actor {name: $actor_name}) RETURN a"
        self.db.run_query(query, {"actor_name": actor_name})
    
    def create_release_year(self, release_year):
        query = "MERGE (y:Year {year: $release_year}) RETURN y"
        self.db.run_query(query, {"release_year": release_year})
    
    def create_runtime(self, runtime):
        query = "MERGE (r:Runtime {minutes: $runtime}) RETURN r"
        self.db.run_query(query, {"runtime": runtime})
    
    def create_relationships(self, title, genres, companies, countries, language, popularity, director, actors, release_year, runtime):
        for genre in genres:
            query = """
            MATCH (m:Movie {title: $title}), (g:Genre {name: $genre})
            MERGE (m)-[:BELONGS_TO]->(g)
            """
            self.db.run_query(query, {"title": title, "genre": genre})
        
        for company in companies:
            query = """
            MATCH (m:Movie {title: $title}), (c:ProductionCompany {name: $company})
            MERGE (m)-[:PRODUCED_BY]->(c)
            """
            self.db.run_query(query, {"title": title, "company": company})
        
        for country in countries:
            query = """
            MATCH (m:Movie {title: $title}), (p:ProductionCountry {name: $country})
            MERGE (m)-[:PRODUCED_IN]->(p)
            """
            self.db.run_query(query, {"title": title, "country": country})
        
        query = """
        MATCH (m:Movie {title: $title})
        MERGE (l:Language {name: $language})
        MERGE (m)-[:ORIGINAL_LANGUAGE]->(l)
        """
        self.db.run_query(query, {"title": title, "language": language})
        
        query = """
        MATCH (m:Movie {title: $title})
        MERGE (p:Popularity {score: $popularity})
        MERGE (m)-[:HAS_POPULARITY]->(p)
        """
        self.db.run_query(query, {"title": title, "popularity": popularity})
        
        query = """
        MATCH (m:Movie {title: $title}), (d:Director {name: $director})
        MERGE (m)-[:DIRECTED_BY]->(d)
        """
        self.db.run_query(query, {"title": title, "director": director})
        
        for actor in actors:
            query = """
            MATCH (m:Movie {title: $title}), (a:Actor {name: $actor})
            MERGE (m)-[:FEATURES_ACTOR]->(a)
            """
            self.db.run_query(query, {"title": title, "actor": actor})
        
        query = """
        MATCH (m:Movie {title: $title}), (y:Year {year: $release_year})
        MERGE (m)-[:RELEASED_IN]->(y)
        """
        self.db.run_query(query, {"title": title, "release_year": release_year})
        
        query = """
        MATCH (m:Movie {title: $title}), (r:Runtime {minutes: $runtime})
        MERGE (m)-[:HAS_RUNTIME]->(r)
        """
        self.db.run_query(query, {"title": title, "runtime": runtime})
    
    def load_movies_from_csv(self, file_path):
        df = pd.read_csv(file_path)
        
        for _, row in df.iterrows():
            title = row['original_title']
            language = row['original_language']
            popularity = row['popularity']
            genres = eval(row['genres'])
            companies = eval(row['production_companies'])
            countries = eval(row['production_countries'])
            director = row.get('director', 'Unknown')
            actors = eval(row.get('actors', '[]'))
            release_year = row.get('release_year', 0)
            runtime = row.get('runtime', 0)
            
            self.create_movie(title, language, popularity)
            for genre in genres:
                self.create_genre(genre)
            for company in companies:
                self.create_production_company(company)
            for country in countries:
                self.create_country(country)
            self.create_director(director)
            for actor in actors:
                self.create_actor(actor)
            self.create_release_year(release_year)
            self.create_runtime(runtime)
            
            self.create_relationships(title, genres, companies, countries, language, popularity, director, actors, release_year, runtime)
        
        print("Carga de datos completada.")

# Conexión con Neo4j
neo4j_conn = Neo4jConnection(uri="neo4j+s://82bfff13.databases.neo4j.io", user="neo4j", password="UWNeGWrYs_UYFO_24dOPHgv-SGQomV9wHOQdsWOyh10")
db = MovieDatabase(neo4j_conn)

# Cargar datos desde el CSV
db.load_movies_from_csv("cleaned_movies.csv")

# Cerrar conexión
neo4j_conn.close()
