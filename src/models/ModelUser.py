from .entities.User import User
from sqlalchemy.sql import text


class ModelUser():
    @classmethod
    def login(self, user, db):
        try:
            with db.connect() as cursor:
                sql = f"""SELECT * FROM ventas.user where email = '{user.email}'"""
                row = cursor.execute(text(sql)).fetchone()
               
                if row:
                    print(row[2])
                    user = User(row[0], row[1], User.check_password(row[2], user.password), row[3], row[4], row[5],row[6])
                    return user
                
                else:
                    return None


        except Exception as e:
            raise Exception(e)
        
    @classmethod
    def get_user_by_id(self, id, db):
        
        try:
            with db.connect() as cursor:
                sql = text("SELECT iduser,username, email,tokens,costtokens,typeUsers FROM ventas.user where iduser = :id")
                row = cursor.execute(sql, {"id":id}).fetchone()
               
                if row:
                    return  User(row[0], row[1],None, row[2], row[3], row[4],row[5])
                    
                
                else:
                    return None


        except Exception as e:
            raise Exception(e)