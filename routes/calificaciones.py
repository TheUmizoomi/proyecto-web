from flask import Blueprint, flash, redirect, render_template, request, url_for

from models.calificaciones_model import (
    create_calificacion,
    delete_calificacion,
    list_calificaciones,
    update_calificacion,
)
from models.docentes_model import list_docentes
from models.materias_model import list_materias
from models.alumnos_model import list_alumnos
from routes.validators import clean_text, obtener_periodo_actual, parse_float

calificaciones_bp = Blueprint("calificaciones", __name__)


def _calificacion_valida(calificacion):
    return calificacion is not None and 0 <= calificacion <= 100


@calificaciones_bp.route("/", methods=["GET", "POST"])
def calificaciones():
    if request.method == "POST":
        alumno_id = clean_text(request.form.get("alumno_id"))
        materia_id = clean_text(request.form.get("materia_id"))
        docente_id = clean_text(request.form.get("docente_id"))
        calificacion = parse_float(request.form.get("calificacion"))
        periodo = obtener_periodo_actual()

        if (
            not alumno_id
            or not materia_id
            or not docente_id
            or not _calificacion_valida(calificacion)
        ):
            flash("Datos inválidos", "danger")
        else:
            ok, err = create_calificacion(
                {
                    "alumno_id": alumno_id,
                    "materia_id": materia_id,
                    "docente_id": docente_id,
                    "calificacion": calificacion,
                    "periodo": periodo,
                }
            )
            if ok:
                flash("Calificación registrada", "success")
                return redirect(url_for("calificaciones.calificaciones"))
            flash("Operación no permitida" if err else "Datos inválidos", "danger")

    return render_template(
        "calificaciones.html",
        calificaciones=list_calificaciones(),
        alumnos=list_alumnos(),
        materias=list_materias(),
        docentes=list_docentes(),
        periodo_actual=obtener_periodo_actual(),
    )


@calificaciones_bp.route("/eliminar/<calificacion_id>", methods=["POST"])
def eliminar_calificacion(calificacion_id):
    parsed_id = clean_text(calificacion_id)
    if not parsed_id:
        flash("Registro no encontrado", "warning")
        return redirect(url_for("calificaciones.calificaciones"))

    ok, err = delete_calificacion(parsed_id)
    if ok:
        flash("Calificación eliminada", "success")
    else:
        flash(err or "Registro no encontrado", "danger")
    return redirect(url_for("calificaciones.calificaciones"))


@calificaciones_bp.route("/editar/<calificacion_id>", methods=["POST"])
def editar_calificacion(calificacion_id):
    parsed_id = clean_text(calificacion_id)
    calificacion = parse_float(request.form.get("calificacion"))
    periodo = obtener_periodo_actual()

    if not parsed_id:
        flash("Registro no encontrado", "warning")
        return redirect(url_for("calificaciones.calificaciones"))
    if not _calificacion_valida(calificacion):
        flash("Datos inválidos", "danger")
        return redirect(url_for("calificaciones.calificaciones"))

    ok, err = update_calificacion(parsed_id, calificacion, periodo)
    if ok:
        flash("Calificación actualizada", "success")
    else:
        flash(err or "Registro no encontrado", "danger")
    return redirect(url_for("calificaciones.calificaciones"))
