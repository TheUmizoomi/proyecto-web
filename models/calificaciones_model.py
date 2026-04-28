from models.db import alumnos_col, calificaciones_col, docentes_col, materias_col, to_object_id


def _nombre_alumno(doc):
    if not doc:
        return "N/A"
    ap_pat = doc.get("apellido_paterno", doc.get("paterno", ""))
    ap_mat = doc.get("apellido_materno", doc.get("materno", ""))
    return f"{doc.get('nombre', '')} {ap_pat} {ap_mat}".strip()


def _to_detail(item):
    alumno = alumnos_col.find_one({"_id": item.get("alumno_id")})
    materia = materias_col.find_one({"_id": item.get("materia_id")})
    docente = docentes_col.find_one({"_id": item.get("docente_id")})
    return {
        "id": str(item["_id"]),
        "_id": str(item["_id"]),
        "alumno_id": str(item.get("alumno_id")) if item.get("alumno_id") else "",
        "materia_id": str(item.get("materia_id")) if item.get("materia_id") else "",
        "docente_id": str(item.get("docente_id")) if item.get("docente_id") else "",
        "alumno": _nombre_alumno(alumno),
        "materia": materia.get("nombre", "N/A") if materia else "N/A",
        "docente": _nombre_alumno(docente),
        "calificacion": item.get("calificacion"),
        "periodo": item.get("periodo", ""),
    }


def list_calificaciones():
    try:
        data = [_to_detail(item) for item in calificaciones_col.find()]
        return sorted(data, key=lambda x: (x.get("alumno", ""), x.get("materia", "")))
    except Exception:
        return []


def create_calificacion(data):
    try:
        alumno_oid = to_object_id(data.get("alumno_id"))
        materia_oid = to_object_id(data.get("materia_id"))
        docente_oid = to_object_id(data.get("docente_id"))
        if alumno_oid is None or materia_oid is None or docente_oid is None:
            return False, "Datos inválidos"
        if not alumnos_col.find_one({"_id": alumno_oid}, {"_id": 1}):
            return False, "Alumno no encontrado"
        if not materias_col.find_one({"_id": materia_oid}, {"_id": 1}):
            return False, "Materia no encontrada"
        if not docentes_col.find_one({"_id": docente_oid}, {"_id": 1}):
            return False, "Docente no encontrado"

        calificaciones_col.insert_one(
            {
                "alumno_id": alumno_oid,
                "materia_id": materia_oid,
                "docente_id": docente_oid,
                "calificacion": float(data.get("calificacion")),
                "periodo": str(data.get("periodo", "")).strip().upper(),
            }
        )
        return True, None
    except Exception as error:
        return False, str(error)


def delete_calificacion(id):
    try:
        oid = to_object_id(id)
        if oid is None:
            return False, "Registro no encontrado"
        result = calificaciones_col.delete_one({"_id": oid})
        return result.deleted_count > 0, None
    except Exception as error:
        return False, str(error)


def update_calificacion(id, calificacion, periodo):
    try:
        oid = to_object_id(id)
        if oid is None:
            return False, "Registro no encontrado"
        result = calificaciones_col.update_one(
            {"_id": oid},
            {
                "$set": {
                    "calificacion": float(calificacion),
                    "periodo": str(periodo).strip().upper(),
                }
            },
        )
        return result.matched_count > 0, None
    except Exception as error:
        return False, str(error)


def get_calificaciones_por_alumno(alumno_id):
    try:
        oid = to_object_id(alumno_id)
        if oid is None:
            return []
        data = [_to_detail(item) for item in calificaciones_col.find({"alumno_id": oid})]
        return sorted(data, key=lambda x: (x.get("periodo", ""), x.get("materia", "")))
    except Exception:
        return []


def save_calificaciones_por_alumno(alumno_id, lista_calificaciones):
    try:
        alumno_oid = to_object_id(alumno_id)
        if alumno_oid is None:
            return False, "Alumno no encontrado"

        for item in lista_calificaciones:
            materia_oid = to_object_id(item.get("materia_id"))
            if materia_oid is None:
                continue

            update_data = {
                "alumno_id": alumno_oid,
                "materia_id": materia_oid,
                "calificacion": float(item.get("calificacion")),
                "periodo": str(item.get("periodo", "")).strip().upper(),
            }

            docente_id = item.get("docente_id")
            docente_oid = to_object_id(docente_id) if docente_id else None
            if docente_oid is not None:
                update_data["docente_id"] = docente_oid

            calificaciones_col.update_one(
                {"alumno_id": alumno_oid, "materia_id": materia_oid},
                {"$set": update_data},
                upsert=True,
            )

        return True, None
    except Exception as error:
        return False, str(error)
