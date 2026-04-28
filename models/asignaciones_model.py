from models.db import alumnos_col, asignaciones_col, materias_col, to_object_id


def _asignacion_detalle(asignacion):
    alumno = alumnos_col.find_one({"_id": asignacion["alumno_id"]})
    materia = materias_col.find_one({"_id": asignacion["materia_id"]})
    return {
        "id": str(asignacion["_id"]),
        "_id": str(asignacion["_id"]),
        "alumno": alumno["nombre"] if alumno else "N/A",
        "apellido_paterno": alumno.get("apellido_paterno", "") if alumno else "",
        "apellido_materno": alumno.get("apellido_materno", "") if alumno else "",
        "matricula": alumno.get("matricula", "") if alumno else "",
        "materia": materia["nombre"] if materia else "N/A",
    }


def create_asignacion(alumno_id: int, materia_id: int):
    alumno_oid = to_object_id(alumno_id)
    materia_oid = to_object_id(materia_id)
    if alumno_oid is None or materia_oid is None:
        return False, None
    if not alumnos_col.find_one({"_id": alumno_oid}) or not materias_col.find_one({"_id": materia_oid}):
        return False, None
    if asignaciones_col.find_one({"alumno_id": alumno_oid, "materia_id": materia_oid}):
        return False, "Operación no permitida"
    asignaciones_col.insert_one({"alumno_id": alumno_oid, "materia_id": materia_oid})
    return True, None


def list_asignaciones():
    asignaciones = [_asignacion_detalle(item) for item in asignaciones_col.find()]
    return sorted(asignaciones, key=lambda item: (item["alumno"], item["materia"]))


def get_asignaciones_por_alumno(alumno_id: int):
    alumno_oid = to_object_id(alumno_id)
    if alumno_oid is None:
        return []
    asignaciones = []
    for item in asignaciones_col.find({"alumno_id": alumno_oid}):
        materia = materias_col.find_one({"_id": item["materia_id"]})
        asignaciones.append(
            {
                "id": str(item["_id"]),
                "_id": str(item["_id"]),
                "materia": materia["nombre"] if materia else "N/A",
            }
        )
    return sorted(asignaciones, key=lambda item: item["materia"])
