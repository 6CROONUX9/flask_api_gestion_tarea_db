from app import db
from app.models.priority import Priority  # Asegúrate de tener el modelo Priority importado

class PriorityService:
    """Servicio para manejar las operaciones CRUD y adicionales para prioridades."""

    @staticmethod
    def create_priority(name):
        """Crear una nueva prioridad en la base de datos.
        
        Args:
            name (str): El nombre de la nueva prioridad.

        Returns:
            Priority: La nueva prioridad creada.

        Raises:
            ValueError: Si la prioridad ya existe.
        """
        # Verificar si la prioridad ya existe
        priority = Priority.query.filter_by(name=name).first()
        if priority:
            raise ValueError("Priority already exists")
        
        # Crear una nueva prioridad
        new_priority = Priority(name=name)
        
        # Guardar la prioridad en la base de datos
        db.session.add(new_priority)
        db.session.commit()
        
        return new_priority

    @staticmethod
    def get_all_priorities():
        """Obtener todas las prioridades disponibles.
        
        Returns:
            List[Priority]: Lista de todas las prioridades en la base de datos.
        """
        # Retorna todas las prioridades
        return Priority.query.all()

    @staticmethod
    def get_priority_by_id(priority_id):
        """Obtener una prioridad por su ID.
        
        Args:
            priority_id (int): El ID de la prioridad.

        Returns:
            Priority: La prioridad correspondiente al ID, o None si no existe.
        """
        # Buscar la prioridad por su ID
        return Priority.query.get(priority_id)

    @staticmethod
    def update_priority(priority_id, new_name):
        """Actualizar el nombre de una prioridad existente.
        
        Args:
            priority_id (int): El ID de la prioridad a actualizar.
            new_name (str): El nuevo nombre para la prioridad.

        Returns:
            Priority: La prioridad actualizada.

        Raises:
            ValueError: Si la prioridad no se encuentra.
        """
        # Buscar la prioridad por su ID
        priority = Priority.query.get(priority_id)
        if not priority:
            raise ValueError("Priority not found")
        
        # Actualizar el nombre de la prioridad
        priority.name = new_name
        
        # Confirmar los cambios en la base de datos
        db.session.commit()
        
        return priority

    @staticmethod
    def delete_priority(priority_id):
        """Eliminar una prioridad existente de la base de datos.
        
        Args:
            priority_id (int): El ID de la prioridad a eliminar.

        Raises:
            ValueError: Si la prioridad no se encuentra.
        """
        # Buscar la prioridad por su ID
        priority = Priority.query.get(priority_id)
        if not priority:
            raise ValueError("Priority not found")
        
        # Eliminar la prioridad
        db.session.delete(priority)
        db.session.commit()