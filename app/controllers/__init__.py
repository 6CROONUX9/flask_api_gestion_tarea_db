from flask import Blueprint
from flask_restx import Api
from .user_controller import user_ns  # Importar el namespace de user_controller
from .task_controller import task_ns  # Importar el namespace de task_controller (si existe)
from .category_controller import category_ns  # Importar el namespace de category_controller (si existe)
from .priority_controller import priority_ns  # Importar el namespace de priority_controller (si existe)
from .auth_controller import auth_ns  # Importar el namespace de auth_controller (si existe)

# Crear un objeto Blueprint para los controladores
blueprint = Blueprint('api', __name__)

# Crear un objeto Api de Flask-RESTx
api = Api(blueprint, version='1.0', title='API de Gestión', description='API para gestión de usuarios, tareas, categorías y prioridades')

# Registrar los namespaces en la API
api.add_namespace(user_ns)  # Registrar el namespace de usuarios
api.add_namespace(task_ns)  # Registrar el namespace de tareas
api.add_namespace(category_ns)  # Registrar el namespace de categorías
api.add_namespace(priority_ns)  # Registrar el namespace de prioridades
api.add_namespace(auth_ns)  # Registrar el namespace de autenticación

