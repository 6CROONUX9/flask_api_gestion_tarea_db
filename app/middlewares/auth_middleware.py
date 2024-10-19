from flask_jwt_extended import get_jwt_identity
from functools import wraps
from flask import jsonify
from app.services.user_service import UserService

def priority_required(required_priority):
    """
    Middleware personalizado para verificar si el usuario autenticado tiene una prioridad específica.
    
    Args:
        required_priority (str): La prioridad requerida que se debe cumplir para acceder al recurso.
    
    Returns:
        Función decoradora que protege el endpoint y restringe el acceso si la prioridad no es adecuada.
    """
    
    def decorator(func):
        @wraps(func)  # Mantiene el nombre y la docstring original de la función decorada
        def wrapper(*args, **kwargs):
            # Obtener el nombre de usuario (identity) del token JWT actual
            username = get_jwt_identity()
            
            # Buscar el usuario en la base de datos por su nombre de usuario
            user = UserService.get_user_by_username(username)
            
            # Verificar si la prioridad del usuario coincide con la prioridad requerida
            # En este caso, deberías tener una forma de obtener la prioridad del usuario
            # Esto podría ser una propiedad en el modelo de usuario o a través de un servicio
            user_priority = user.priority.name if user.priority else None
            
            if user_priority != required_priority:
                # Si la prioridad no coincide, retornar un mensaje de error y un código de estado 403
                return jsonify({"message": "Acceso denegado: prioridad insuficiente"}), 403
            
            # Si la prioridad es correcta, continuar con la ejecución del endpoint
            return func(*args, **kwargs)
        
        return wrapper  # Retorna la función decorada con las verificaciones de prioridad
    return decorator  # Retorna el decorador
