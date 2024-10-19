from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from app.services.priority_service import PriorityService

# Crear un espacio de nombres (namespace) para prioridades
priority_ns = Namespace('priorities', description='Operaciones relacionadas con las prioridades')

# Definir el modelo de entrada de prioridad para la documentación de Swagger
priority_model = priority_ns.model('Priority', {
    'name': fields.String(required=True, description='Nombre de la prioridad')
})

# Definir el modelo de salida de prioridad para la documentación de Swagger
priority_response_model = priority_ns.model('PriorityResponse', {
    'id': fields.Integer(description='ID de la prioridad'),
    'name': fields.String(description='Nombre de la prioridad')
})

# Controlador para manejar las operaciones CRUD de prioridades
@priority_ns.route('/')
class PriorityListResource(Resource):
    @priority_ns.doc('get_priorities')
    @priority_ns.marshal_list_with(priority_response_model)  # Formato de respuesta
    def get(self):
        """Obtener todas las prioridades"""
        priorities = PriorityService.get_all_priorities()
        return priorities, 200

    @priority_ns.doc('create_priority')
    @priority_ns.expect(priority_model, validate=True)  # Modelo esperado
    @priority_ns.marshal_with(priority_response_model, code=201)  # Formato de respuesta
    def post(self):
        """Crear una nueva prioridad"""
        data = request.get_json()
        try:
            priority = PriorityService.create_priority(data['name'])
            return priority, 201
        except ValueError as e:
            return {'message': str(e)}, 400

@priority_ns.route('/<int:priority_id>')
@priority_ns.param('priority_id', 'El ID de la prioridad')
class PriorityResource(Resource):
    @priority_ns.doc('get_priority_by_id')
    @priority_ns.marshal_with(priority_response_model)
    def get(self, priority_id):
        """Obtener una prioridad por su ID"""
        priority = PriorityService.get_priority_by_id(priority_id)
        if not priority:
            return {'message': 'Prioridad no encontrada'}, 404
        return priority, 200

    @priority_ns.doc('update_priority')
    @priority_ns.expect(priority_model, validate=True)  # Nuevos datos de prioridad
    @priority_ns.marshal_with(priority_response_model)
    def put(self, priority_id):
        """Actualizar una prioridad por su ID"""
        data = request.get_json()
        try:
            priority = PriorityService.update_priority(priority_id, data['name'])
            return priority, 200
        except ValueError as e:
            return {'message': str(e)}, 404

    @priority_ns.doc('delete_priority')
    def delete(self, priority_id):
        """Eliminar una prioridad por su ID"""
        try:
            PriorityService.delete_priority(priority_id)
            return {'message': 'Prioridad eliminada exitosamente'}, 200
        except ValueError as e:
            return {'message': str(e)}, 404
