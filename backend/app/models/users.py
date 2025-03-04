class User:
    def __init__(self, name, age, email):
        self.name = name
        self.age = age
        self.email = email
        
    def to_dict(self):
        return {
            "name" : self.name,
            "age" : self.age,
            "email" : self.email
        }