from app import db

class Category(db.Model):
    """
    Modelo que representa una categoría en el sistema.

    Cada categoría puede estar asociada a varias tareas, ayudando a organizarlas por grupos temáticos o funcionales.

    Atributos:
        id (int): Identificador único de la categoría (clave primaria).
        name (str): Nombre de la categoría, debe ser único y no nulo.
    """
    
    __tablename__ = 'categories'  # Nombre de la tabla en la base de datos

    # Definición de columnas de la tabla
    id = db.Column(db.Integer, primary_key=True)  # Clave primaria de la tabla
    name = db.Column(db.String(100), unique=True, nullable=False)  # Nombre de la categoría, debe ser único y no nulo

    def __init__(self, name):
        """
        Constructor de la clase Category.
        
        Args:
            name (str): El nombre de la categoría.
        """
        self.name = name

    def __repr__(self):
        """
        Representación en cadena del objeto Category.
        
        Returns:
            str: Nombre de la categoría.
        """
        return f'<Category {self.name}>'

    def to_dict(self):
        """
        Convierte el objeto Category en un diccionario.

        Returns:
            dict: Representación del objeto en forma de diccionario.
        """
        return {
            'id': self.id,
            'name': self.name
        }
