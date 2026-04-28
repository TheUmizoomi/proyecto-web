from models.db import alumnos_col, asignaciones_col, calificaciones_col, materias_col, to_object_id


def reporte_por_alumno(alumno_id: int):
    alumno_oid = to_object_id(alumno_id)
    if alumno_oid is None:
        return []
    alumno = alumnos_col.find_one({"_id": alumno_oid})
    if not alumno:
        return []

    filas = []
    asignaciones = list(asignaciones_col.find({"alumno_id": alumno_oid}))
    if not asignaciones:
        return [
            {
                "id": str(alumno["_id"]),
                "alumno": alumno["nombre"],
                "matricula": alumno.get("matricula", ""),
                "carrera": alumno.get("carrera", ""),
                "materia": None,
                "calificacion": None,
            }
        ]
    for asignacion in asignaciones:
        materia = materias_col.find_one({"_id": asignacion["materia_id"]})
        calificacion = calificaciones_col.find_one({"alumno_materia_id": asignacion["_id"]})
        filas.append(
            {
                "id": str(alumno["_id"]),
                "alumno": alumno["nombre"],
                "matricula": alumno.get("matricula", ""),
                "carrera": alumno.get("carrera", ""),
                "materia": materia["nombre"] if materia else None,
                "calificacion": calificacion["calificacion"] if calificacion else None,
            }
        )
    return sorted(filas, key=lambda item: (item["materia"] or ""))


def reporte_general():
    filas = []
    for alumno in alumnos_col.find():
        asignaciones = list(asignaciones_col.find({"alumno_id": alumno["_id"]}))
        if not asignaciones:
            filas.append(
                {
                    "alumno": alumno["nombre"],
                    "matricula": alumno.get("matricula", ""),
                    "carrera": alumno.get("carrera", ""),
                    "materia": None,
                    "calificacion": None,
                }
            )
            continue
        for asignacion in asignaciones:
            materia = materias_col.find_one({"_id": asignacion["materia_id"]})
            calificacion = calificaciones_col.find_one({"alumno_materia_id": asignacion["_id"]})
            filas.append(
                {
                    "alumno": alumno["nombre"],
                    "matricula": alumno.get("matricula", ""),
                    "carrera": alumno.get("carrera", ""),
                    "materia": materia["nombre"] if materia else None,
                    "calificacion": calificacion["calificacion"] if calificacion else None,
                }
            )
    return sorted(filas, key=lambda item: (item["alumno"], item["materia"] or ""))
