class Movie:
    def __init__(self, title, language, popularity):
        self.title = title
        self.language = language
        self.popularity = popularity

    def to_dict(self):
        return {
            "title": self.title,
            "language": self.language,
            "popularity": self.popularity
        }
