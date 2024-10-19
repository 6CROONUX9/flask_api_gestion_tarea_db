from flask import current_app
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from app import db
from app.models.user import User

from werkzeug.security import check_password_hash

class AuthService:
    """Servicio para manejar la autenticación de usuarios."""

    def __init__(self):
        self.jwt = JWTManager(current_app)

    def register_user(self, username, password, role_id):
        """Registrar un nuevo usuario y crear su token de acceso.
        
        Args:
            username (str): Nombre de usuario del nuevo usuario.
            password (str): Contraseña en texto plano que será encriptada.
            role_id (int): ID del rol que se asociará al usuario.

        Returns:
            str: Token de acceso JWT para el usuario registrado.

        Raises:
            ValueError: Si el nombre de usuario ya existe o el rol no se encuentra.
        """
        # Verificar si el nombre de usuario ya existe
        if User.query.filter_by(username=username).first():
            raise ValueError("Username already exists")

        # Verificar si el rol existe
        role = Role.query.get(role_id)
        if not role:
            raise ValueError("Role not found")

        # Crear un nuevo usuario
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, password=hashed_password, role_id=role_id)
        db.session.add(new_user)
        db.session.commit()

        # Crear y devolver el token
        return create_access_token(identity=new_user.username)

    def login_user(self, username, password):
        """Iniciar sesión para un usuario existente y generar un token de acceso.
        
        Args:
            username (str): Nombre de usuario del usuario.
            password (str): Contraseña del usuario.

        Returns:
            str: Token de acceso JWT si la autenticación es exitosa.

        Raises:
            ValueError: Si el nombre de usuario no existe o la contraseña es incorrecta.
        """
        # Buscar al usuario por su nombre de usuario
        user = User.query.filter_by(username=username).first()
        if not user or not check_password_hash(user.password, password):
            raise ValueError("Invalid username or password")

        # Crear y devolver el token
        return create_access_token(identity=user.username)

    @jwt_required()
    def get_current_user(self):
        """Obtener el usuario actualmente autenticado.
        
        Returns:
            User: El usuario actualmente autenticado.
        """
        current_username = get_jwt_identity()
        return User.query.filter_by(username=current_username).first()

    @jwt_required()
    def logout_user(self):
        """Cerrar sesión del usuario actual.
        
        Returns:
            str: Mensaje de éxito.
        """
        # Implementar lógica de cierre de sesión si es necesario
        return "Logout successful"
