from app import db

class User(db.Model):
    """
    Modelo que representa un usuario en el sistema.

    Cada usuario tiene un nombre de usuario y una contraseña encriptada.
    
    Atributos:
        id (int): Identificador único del usuario (clave primaria).
        username (str): Nombre de usuario, debe ser único.
        password (str): Contraseña encriptada del usuario.
    """
    
    __tablename__ = 'users'  # Especifica el nombre de la tabla en la base de datos

    # Definición de columnas de la tabla
    id = db.Column(db.Integer, primary_key=True)  # Clave primaria de la tabla
    username = db.Column(db.String(80), unique=True, nullable=False)  # Nombre de usuario, debe ser único y no nulo
    password = db.Column(db.String(120), nullable=False)  # Contraseña encriptada del usuario, no puede ser nula

    def __init__(self, username, password):
        """
        Constructor de la clase User.

        Args:
            username (str): El nombre de usuario.
            password (str): La contraseña encriptada.
        """
        self.username = username
        self.password = password

    def __repr__(self):
        """
        Representación en cadena del objeto User.
        
        Returns:
            str: Nombre de usuario.
        """
        return f'<User {self.username}>'

    def to_dict(self):
        """
        Convierte el objeto User en un diccionario.

        Returns:
            dict: Representación del objeto en forma de diccionario.
        """
        return {
            'id': self.id,
            'username': self.username
        }
