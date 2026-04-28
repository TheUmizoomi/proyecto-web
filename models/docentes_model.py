from models.db import docentes_col, to_object_id


def _with_id(doc):
    if not doc:
        return None
    doc["_id"] = str(doc["_id"])
    doc["id"] = doc["_id"]
    return doc


def list_docentes():
    try:
        docentes = list(docentes_col.find().sort("nombre", 1))
        return [_with_id(docente) for docente in docentes]
    except Exception:
        return []


def get_docente(docente_id: int):
    try:
        oid = to_object_id(docente_id)
    except Exception:
        return None
    if oid is None:
        return None
    try:
        return _with_id(docentes_col.find_one({"_id": oid}))
    except Exception:
        return None


def create_docente(
    nombre: str,
    paterno: str,
    materno: str,
    correo: str,
    telefono: str = None,
    grado_academico: str = None,
):
    try:
        if docentes_col.find_one({"correo": correo}):
            return False, "Operación no permitida"
        docentes_col.insert_one(
            {
                "nombre": nombre,
                "paterno": paterno,
                "materno": materno,
                "correo": correo,
                "telefono": telefono,
                "grado_academico": grado_academico,
            }
        )
        return True, None
    except Exception as error:
        return False, str(error)


def update_docente(
    docente_id: int,
    nombre: str,
    paterno: str,
    materno: str,
    correo: str,
    telefono: str = None,
    grado_academico: str = None,
):
    try:
        oid = to_object_id(docente_id)
        if oid is None:
            return False, None
        duplicado = docentes_col.find_one({"correo": correo, "_id": {"$ne": oid}}, {"_id": 1})
        if duplicado:
            return False, "Operación no permitida"
        result = docentes_col.update_one(
            {"_id": oid},
            {
                "$set": {
                    "nombre": nombre,
                    "paterno": paterno,
                    "materno": materno,
                    "correo": correo,
                    "telefono": telefono,
                    "grado_academico": grado_academico,
                }
            },
        )
        return result.matched_count > 0, None
    except Exception as error:
        return False, str(error)


def delete_docente(docente_id: int):
    try:
        oid = to_object_id(docente_id)
        if oid is None:
            return False, None
        result = docentes_col.delete_one({"_id": oid})
        return result.deleted_count > 0, None
    except Exception as error:
        return False, str(error)
