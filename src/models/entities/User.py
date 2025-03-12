from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin):

    def __init__(self, id, username, password, email,tokens,costtokens,typeUsers) -> None:
        self.id = id
        self.username = username
        self.password = password
        self.email = email
        self.tokens = tokens
        self.costtokens = costtokens
        self.typeUsers = typeUsers

    def __str__(self):
        return f'User: {self.username}'

    def __repr__(self):
        return f'User: {self.username}'
    
    @classmethod
    def check_password(self, password, hashed_password):
        
        return check_password_hash(password, hashed_password)
        
  
