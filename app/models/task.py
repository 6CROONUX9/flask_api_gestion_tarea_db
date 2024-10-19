from app import db

# Tabla intermedia para la relación de muchos a muchos entre Tareas y Categorías
task_category = db.Table('task_category',
    db.Column('task_id', db.Integer, db.ForeignKey('tasks.id'), primary_key=True),  # Referencia a la tabla 'tasks'
    db.Column('category_id', db.Integer, db.ForeignKey('categories.id'), primary_key=True)  # Referencia a la tabla 'categories'
)

class Task(db.Model):
    """
    Modelo que representa una tarea en el sistema.

    Cada tarea puede estar asociada a múltiples categorías y contiene información como el título, descripción y estado de completada.

    Atributos:
        id (int): Identificador único de la tarea (clave primaria).
        title (str): Título de la tarea.
        description (str): Descripción detallada de la tarea (opcional).
        completed (bool): Indica si la tarea está completada o no.
        priority_id (int): Clave foránea hacia la tabla 'priorities' para definir la prioridad de la tarea.
        categories (list): Relación muchos a muchos con la tabla de categorías.
    """
    
    __tablename__ = 'tasks'  # Nombre de la tabla en la base de datos

    # Definición de columnas de la tabla
    id = db.Column(db.Integer, primary_key=True)  # Clave primaria de la tabla
    title = db.Column(db.String(120), nullable=False)  # Título de la tarea, no puede ser nulo
    description = db.Column(db.String(255), nullable=True)  # Descripción de la tarea, es opcional
    completed = db.Column(db.Boolean, default=False, nullable=False)  # Estado de la tarea (completada o no), por defecto False
    priority_id = db.Column(db.Integer, db.ForeignKey('priorities.id'), nullable=False)  # Clave foránea hacia la tabla 'priorities'

    # Relación muchos a muchos con categorías usando la tabla intermedia 'task_category'
    categories = db.relationship('Category', 
                                 secondary=task_category,  # Tabla intermedia que define la relación
                                 backref=db.backref('tasks', lazy=True))  # Permite acceso inverso desde categorías a tareas

    # Relación con el modelo Priority
    priority = db.relationship('Priority', backref='tasks')  # Define la relación con el modelo Priority

    def __init__(self, title, description=None, completed=False, priority_id=None):
        """
        Constructor de la clase Task.

        Args:
            title (str): El título de la tarea.
            description (str, opcional): La descripción de la tarea.
            completed (bool, opcional): Indica si la tarea está completada o no, por defecto es False.
            priority_id (int, opcional): El ID de la prioridad asociada a la tarea.
        """
        self.title = title
        self.description = description
        self.completed = completed
        self.priority_id = priority_id  # Asigna el ID de prioridad si se proporciona

    def __repr__(self):
        """
        Representación en cadena del objeto Task.
        
        Returns:
            str: Título de la tarea y su estado.
        """
        return f'<Task {self.title} - Completed: {self.completed}>'

    def to_dict(self):
        """
        Convierte el objeto Task en un diccionario.

        Returns:
            dict: Representación del objeto en forma de diccionario, incluyendo prioridades y categorías.
        """
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'completed': self.completed,
            'priority': self.priority.name if self.priority else None,  # Incluye la prioridad si existe
            'categories': [category.to_dict() for category in self.categories]  # Serializa las categorías
        }