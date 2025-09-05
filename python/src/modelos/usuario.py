from flask_login import UserMixin

class Usuario(UserMixin):

    def __init__(self, usuario:str, nombre:str, admin:bool)->None:

        self.id=usuario
        self.nombre=nombre
        self.admin=admin