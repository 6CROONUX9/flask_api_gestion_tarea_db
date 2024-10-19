from app import db

class Priority(db.Model):
    """
    Modelo que representa una prioridad en el sistema.

    Cada prioridad puede estar asociada a múltiples tareas, ayudando a definir el nivel de urgencia o importancia de cada tarea.

    Atributos:
        id (int): Identificador único de la prioridad (clave primaria).
        name (str): Nombre de la prioridad, debe ser único (ej: 'Alta', 'Media', 'Baja').
    """

    __tablename__ = 'priorities'  # Nombre de la tabla en la base de datos

    # Definición de columnas de la tabla
    id = db.Column(db.Integer, primary_key=True)  # Clave primaria de la tabla
    name = db.Column(db.String(50), unique=True, nullable=False)  # Nombre de la prioridad, debe ser único y no nulo

    def __init__(self, name):
        """
        Constructor de la clase Priority.

        Args:
            name (str): El nombre de la prioridad (ej: 'Alta', 'Media', 'Baja').
        """
        self.name = name
