from bson.objectid import ObjectId
from pymongo import MongoClient
import os

MONGO_URI = os.getenv("MONGO_URI")

_mongo_client = MongoClient(MONGO_URI)

mongo_db = _mongo_client["control_academico"]

alumnos_col = mongo_db["alumnos"]
docentes_col = mongo_db["docentes"]
materias_col = mongo_db["materias"]
asignaciones_col = mongo_db["alumno_materia"]
calificaciones_col = mongo_db["calificaciones"]


def to_object_id(value):
    if isinstance(value, ObjectId):
        return value
    if not value:
        return None
    try:
        return ObjectId(str(value))
    except Exception:
        return None