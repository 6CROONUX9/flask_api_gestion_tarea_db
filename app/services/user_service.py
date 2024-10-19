from app import db, bcrypt
from app.models.user import User
from sqlalchemy.exc import IntegrityError

class UserService:
    @staticmethod
    def create_user(username, password):
        # Lógica para crear un nuevo usuario
        new_user = User(username=username, password=password)  # Asumiendo que tienes un modelo User
        db.session.add(new_user)
        db.session.commit()
        return new_user  # Asegúrate de que `new_user` sea serializable
    
    @staticmethod
    def get_all_users():
        """
        Obtener todos los usuarios de la base de datos.
        
        Returns:
            List[User]: Lista de todos los usuarios en la base de datos.
        """
        # Recuperar todos los registros de la tabla User
        return User.query.all()

    @staticmethod
    def get_user_by_username(username):
        """
        Obtener un usuario por su nombre de usuario.
        
        Args:
            username (str): Nombre de usuario a buscar.
        
        Returns:
            User: El usuario encontrado o None si no existe.
        """
        # Filtrar usuarios por su nombre de usuario (username)
        return User.query.filter_by(username=username).first()

    @staticmethod
    def update_user(username, new_data):
        """
        Actualizar los datos de un usuario existente.
        
        Args:
            username (str): Nombre del usuario a actualizar.
            new_data (dict): Diccionario con los nuevos datos, como 'password'.
        
        Returns:
            None
        
        Raises:
            ValueError: Si el usuario no es encontrado.
        """
        # Buscar al usuario por su nombre de usuario
        user = UserService.get_user_by_username(username)
        if not user:
            # Si no se encuentra el usuario, lanzar una excepción
            raise ValueError('User not found')

        # Si se proporciona una nueva contraseña, generar el hash
        if 'password' in new_data:
            user.password = bcrypt.generate_password_hash(new_data['password']).decode('utf-8')

        # Guardar los cambios en la base de datos
        db.session.commit()

    @staticmethod
    def delete_user(username):
        """
        Eliminar un usuario existente.
        
        Args:
            username (str): Nombre del usuario a eliminar.
        
        Returns:
            None
        
        Raises:
            ValueError: Si el usuario no es encontrado.
        """
        # Buscar al usuario por su nombre de usuario
        user = UserService.get_user_by_username(username)
        if not user:
            # Si no se encuentra el usuario, lanzar una excepción
            raise ValueError('User not found')

        # Eliminar el usuario de la base de datos
        db.session.delete(user)
        db.session.commit()
