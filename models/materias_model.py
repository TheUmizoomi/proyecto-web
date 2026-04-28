from models.db import asignaciones_col, docentes_col, materias_col, to_object_id


def _with_id(doc):
    if not doc:
        return None
    doc["_id"] = str(doc["_id"])
    doc["id"] = doc["_id"]
    if doc.get("docente_id"):
        docente_oid = doc["docente_id"]
        doc["docente_id"] = str(docente_oid)
        docente = docentes_col.find_one({"_id": docente_oid})
        if docente:
            ap_pat = docente.get("apellido_paterno", docente.get("paterno", ""))
            ap_mat = docente.get("apellido_materno", docente.get("materno", ""))
            doc["docente_nombre"] = f"{docente.get('nombre', '')} {ap_pat} {ap_mat}".strip()
        else:
            doc["docente_nombre"] = "-"
    else:
        doc["docente_nombre"] = "-"
    return doc


def list_materias():
    try:
        materias = list(materias_col.find().sort("nombre", 1))
        return [_with_id(materia) for materia in materias]
    except Exception:
        return []


def get_materia(materia_id: int):
    try:
        oid = to_object_id(materia_id)
    except Exception:
        return None
    if oid is None:
        return None
    try:
        return _with_id(materias_col.find_one({"_id": oid}))
    except Exception:
        return None


def create_materia(
    clave: str,
    nombre: str,
    creditos: int,
    unidades: int,
    carrera: str,
    docente_id: str,
):
    try:
        docente_oid = to_object_id(docente_id)
        if docente_oid is None:
            return False, "Docente no encontrado"
        if not docentes_col.find_one({"_id": docente_oid}, {"_id": 1}):
            return False, "Docente no encontrado"
        if materias_col.find_one({"clave": clave}, {"_id": 1}):
            return False, "Operación no permitida"
        materias_col.insert_one(
            {
                "clave": clave,
                "nombre": nombre,
                "creditos": creditos,
                "unidades": unidades,
                "carrera": carrera,
                "docente_id": docente_oid,
            }
        )
        return True, None
    except Exception as error:
        return False, str(error)


def update_materia(
    materia_id: int,
    clave: str,
    nombre: str,
    creditos: int,
    unidades: int,
    carrera: str,
    docente_id: str,
):
    try:
        oid = to_object_id(materia_id)
        if oid is None:
            return False, None
        docente_oid = to_object_id(docente_id)
        if docente_oid is None:
            return False, "Docente no encontrado"
        if not docentes_col.find_one({"_id": docente_oid}, {"_id": 1}):
            return False, "Docente no encontrado"
        duplicado = materias_col.find_one({"clave": clave, "_id": {"$ne": oid}}, {"_id": 1})
        if duplicado:
            return False, "Operación no permitida"
        result = materias_col.update_one(
            {"_id": oid},
            {
                "$set": {
                    "clave": clave,
                    "nombre": nombre,
                    "creditos": creditos,
                    "unidades": unidades,
                    "carrera": carrera,
                    "docente_id": docente_oid,
                }
            },
        )
        return result.matched_count > 0, None
    except Exception as error:
        return False, str(error)


def delete_materia(materia_id: int):
    try:
        oid = to_object_id(materia_id)
        if oid is None:
            return False, None
        if asignaciones_col.find_one({"materia_id": oid}, {"_id": 1}):
            return False, "Operación no permitida"
        result = materias_col.delete_one({"_id": oid})
        return result.deleted_count > 0, None
    except Exception as error:
        return False, str(error)
