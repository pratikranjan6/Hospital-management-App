from flask import jsonify, request
from flask_jwt_extended import JWTManager
from application.models import User 

jwt = JWTManager()