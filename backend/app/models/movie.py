class Movie :
    def __init__(self, title, year, genre):
        self.title = title
        self.year = year
        self.genre = genre
    
    def to_dict(self):
        return {
            "title": self.title,
            "year": self.year,
            "genre": self.genre
            
        }
        