from flask import Blueprint, flash, redirect, render_template, request, url_for

from models.alumnos_model import list_alumnos
from models.asignaciones_model import (
    create_asignacion,
    get_asignaciones_por_alumno,
    list_asignaciones,
)
from models.materias_model import list_materias
from routes.validators import clean_text

asignaciones_bp = Blueprint("asignaciones", __name__)


@asignaciones_bp.route("/", methods=["GET", "POST"])
def asignaciones():
    selected_alumno = None

    if request.method == "POST":
        alumno_id = clean_text(request.form.get("alumno_id"))
        materia_id = clean_text(request.form.get("materia_id"))
        selected_alumno = alumno_id

        if not alumno_id or not materia_id:
            flash("Datos inválidos", "danger")
        else:
            ok, err = create_asignacion(alumno_id, materia_id)
            if ok:
                flash("Materia asignada correctamente", "success")
                return redirect(url_for("asignaciones.asignaciones"))
            flash("Operación no permitida" if err else "Datos inválidos", "danger")

    if request.args.get("alumno_id"):
        selected_alumno = clean_text(request.args.get("alumno_id"))

    asignadas = []
    if selected_alumno is not None:
        asignadas = get_asignaciones_por_alumno(selected_alumno)

    return render_template(
        "asignaciones.html",
        alumnos=list_alumnos(),
        materias=list_materias(),
        asignaciones=list_asignaciones(),
        selected_alumno=selected_alumno,
        asignadas=asignadas,
    )
