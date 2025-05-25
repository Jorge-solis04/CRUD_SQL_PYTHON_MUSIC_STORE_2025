from .entities.user import User


class ModelUser():
    @classmethod
    def login(self, db, user):
        try:
            cur = db.cursor()
            cur.execute("""SELECT id_user, username, password, fullname FROM usuarios 
                        WHERE username = %s""", (user.username,))
            row = cur.fetchone()
            
            if row is not None:
                # Verifica la contraseña antes de crear el usuario
                if User.check_password(row['password'], user.password):
                    return User(row['id_user'], row['username'], row['password'], row['fullname'])
                else:
                    return None
            else:
                return None
        except Exception as ex:
            raise Exception(ex)