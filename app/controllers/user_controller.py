from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from app.services.user_service import UserService

# Crear un espacio de nombres (namespace) para los usuarios
user_ns = Namespace('users', description='Operaciones relacionadas con los usuarios')

# Definir el modelo de usuario para la documentación de Swagger
user_model = user_ns.model('User', {
    'username': fields.String(required=True, description='Nombre de usuario'),
    'password': fields.String(required=True, description='Contraseña'),
})

# Definir el controlador de usuarios con decoradores para la documentación
@user_ns.route('/')
class UserResource(Resource):
    @user_ns.doc('create_user')
    @user_ns.expect(user_model, validate=True)
    def post(self):
        """
        Crear un nuevo usuario
        ---
        Este método permite crear un nuevo usuario proporcionando el nombre de usuario y la contraseña.
        
        Body Parameters:
        - username: El nombre del usuario a crear.
        - password: La contraseña del usuario.

        Responses:
        - 201: Usuario creado con éxito.
        - 400: Si ocurre un error durante la creación del usuario.
        """
        try:
            data = request.get_json()  # Obtiene los datos en formato JSON del cuerpo de la solicitud
            user = UserService.create_user(data['username'], data['password'])

            if hasattr(user, 'to_dict'):
                user_data = user.to_dict()  # Asegúrate de que `user` tenga un método `to_dict()`
            else:
                user_data = {'username': user.username}  # Ajusta según lo que retorne UserService

            return jsonify({'message': 'User created successfully', 'user': user_data}), 201  # Asegúrate de que esto retorne un diccionario
        except Exception as e:
            print(str(e))  # Imprime el error en la consola
            return jsonify({'message': str(e)}), 500  # Asegúrate de que esto retorne un diccionario

    @user_ns.doc('get_users')
    def get(self):
        """
        Obtener todos los usuarios
        ---
        Este método permite obtener una lista de todos los usuarios registrados en la base de datos.

        Responses:
        - 200: Retorna una lista de nombres de usuarios.
        """
        users = UserService.get_all_users()  # Llama al servicio para obtener todos los usuarios
        return jsonify({'users': [user.username for user in users]}), 200  # Retorna solo los nombres de usuario


@user_ns.route('/<username>')
@user_ns.param('username', 'El nombre del usuario')
class UserDetailResource(Resource):
    @user_ns.doc('delete_user')
    def delete(self, username):
        """
        Eliminar un usuario
        ---
        Este método permite eliminar un usuario existente basado en el nombre de usuario.

        Path Parameters:
        - username: El nombre del usuario a eliminar.

        Responses:
        - 200: Usuario eliminado con éxito.
        - 404: Si el usuario no se encuentra.
        """
        try:
            UserService.delete_user(username)  # Llama al servicio para eliminar al usuario
            return jsonify({'message': 'Usuario eliminado con éxito'}), 200
        except Exception as e:
            return jsonify({'message': str(e)}), 404  # Código 404 si no se encuentra el usuario

    @user_ns.doc('update_user')
    @user_ns.expect(user_model, validate=True)  # Espera el modelo de usuario en la solicitud
    def put(self, username):
        """
        Actualizar un usuario
        ---
        Este método permite actualizar la información de un usuario basado en su nombre de usuario.

        Path Parameters:
        - username: El nombre del usuario que se actualizará.

        Body Parameters:
        - username: El nuevo nombre de usuario (opcional).
        - password: La nueva contraseña (opcional).

        Responses:
        - 200: Usuario actualizado con éxito.
        - 404: Si el usuario no se encuentra.
        """
        try:
            new_data = request.get_json()  # Obtiene los nuevos datos para la actualización
            
            # Llama al servicio para actualizar el usuario
            updated_user = UserService.update_user(username, new_data)  
            return jsonify({'message': 'Usuario actualizado con éxito', 'user': updated_user.username}), 200
        except Exception as e:
            return jsonify({'message': str(e)}), 404  # Código 404 si no se encuentra el usuario
