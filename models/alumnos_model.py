from models.db import alumnos_col, to_object_id


def _serialize_doc(doc):
    if not doc:
        return None
    doc["_id"] = str(doc["_id"])
    doc["id"] = doc["_id"]
    return doc


def list_alumnos():
    try:
        alumnos = list(alumnos_col.find().sort("nombre", 1))
        return [_serialize_doc(doc) for doc in alumnos]
    except Exception:
        return []


def get_alumno(alumno_id: int):
    try:
        oid = to_object_id(alumno_id)
        if oid is None:
            return None
        return _serialize_doc(alumnos_col.find_one({"_id": oid}))
    except Exception:
        return None


def create_alumno(
    matricula: str,
    nombre: str,
    apellido_paterno: str,
    apellido_materno: str,
    carrera: str,
    sexo: str,
    edad: int,
    telefono: str,
):
    try:
        if alumnos_col.find_one({"matricula": matricula}, {"_id": 1}):
            return False, "Operación no permitida"
        alumnos_col.insert_one(
            {
                "matricula": matricula,
                "nombre": nombre,
                "apellido_paterno": apellido_paterno,
                "apellido_materno": apellido_materno,
                "carrera": carrera,
                "sexo": sexo,
                "edad": edad,
                "telefono": telefono,
            }
        )
        return True, None
    except Exception as error:
        return False, str(error)


def update_alumno(
    alumno_id: int,
    matricula: str,
    nombre: str,
    apellido_paterno: str,
    apellido_materno: str,
    carrera: str,
    sexo: str,
    edad: int,
    telefono: str,
):
    try:
        oid = to_object_id(alumno_id)
        if oid is None:
            return False, None
        if alumnos_col.find_one({"matricula": matricula, "_id": {"$ne": oid}}, {"_id": 1}):
            return False, "Operación no permitida"
        result = alumnos_col.update_one(
            {"_id": oid},
            {
                "$set": {
                    "matricula": matricula,
                    "nombre": nombre,
                    "apellido_paterno": apellido_paterno,
                    "apellido_materno": apellido_materno,
                    "carrera": carrera,
                    "sexo": sexo,
                    "edad": edad,
                    "telefono": telefono,
                }
            },
        )
        return result.matched_count > 0, None
    except Exception as error:
        return False, str(error)


def delete_alumno(alumno_id: int):
    try:
        oid = to_object_id(alumno_id)
        if oid is None:
            return False, None
        result = alumnos_col.delete_one({"_id": oid})
        return result.deleted_count > 0, None
    except Exception as error:
        return False, str(error)


def get_detalle_alumno(alumno_id: int):
    return []
