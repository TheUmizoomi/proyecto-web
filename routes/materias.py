from flask import Blueprint, flash, redirect, render_template, request, url_for

from models.materias_model import (
    create_materia,
    delete_materia,
    get_materia,
    list_materias,
    update_materia,
)
from models.docentes_model import list_docentes
from routes.validators import limpiar_texto, validar_solo_numeros

materias_bp = Blueprint("materias", __name__)


@materias_bp.route("/", methods=["GET", "POST"])
def materias():
    if request.method == "POST":
        clave = limpiar_texto(request.form.get("clave")).upper()
        nombre = limpiar_texto(request.form.get("nombre")).upper()
        creditos = limpiar_texto(request.form.get("creditos"))
        unidades = limpiar_texto(request.form.get("unidades"))
        carrera = limpiar_texto(request.form.get("carrera")).upper()
        docente_id = limpiar_texto(request.form.get("docente_id"))
        if (
            not clave
            or not nombre
            or not carrera
            or not docente_id
            or not validar_solo_numeros(creditos)
            or not validar_solo_numeros(unidades)
        ):
            flash("Datos inválidos", "danger")
        else:
            ok, err = create_materia(
                clave,
                nombre,
                int(creditos),
                int(unidades),
                carrera,
                docente_id,
            )
            if ok:
                flash("Materia registrada correctamente", "success")
                return redirect(url_for("materias.materias"))
            flash("Operación no permitida" if err else "Datos inválidos", "danger")

    return render_template(
        "materias.html",
        materias=list_materias(),
        docentes=list_docentes(),
    )


@materias_bp.route("/editar/<materia_id>", methods=["GET", "POST"])
def editar_materia(materia_id):
    parsed_id = limpiar_texto(materia_id)
    if not parsed_id:
        flash("Registro no encontrado", "warning")
        return redirect(url_for("materias.materias"))

    materia = get_materia(parsed_id)
    if not materia:
        flash("Registro no encontrado", "warning")
        return redirect(url_for("materias.materias"))

    if request.method == "POST":
        clave = limpiar_texto(request.form.get("clave")).upper()
        nombre = limpiar_texto(request.form.get("nombre")).upper()
        creditos = limpiar_texto(request.form.get("creditos"))
        unidades = limpiar_texto(request.form.get("unidades"))
        carrera = limpiar_texto(request.form.get("carrera")).upper()
        docente_id = limpiar_texto(request.form.get("docente_id"))
        if (
            not clave
            or not nombre
            or not carrera
            or not docente_id
            or not validar_solo_numeros(creditos)
            or not validar_solo_numeros(unidades)
        ):
            flash("Datos inválidos", "danger")
        else:
            ok, err = update_materia(
                parsed_id,
                clave,
                nombre,
                int(creditos),
                int(unidades),
                carrera,
                docente_id,
            )
            if ok:
                flash("Materia actualizada", "success")
                return redirect(url_for("materias.materias"))
            flash("Operación no permitida" if err else "Datos inválidos", "danger")

    return redirect(url_for("materias.materias"))


@materias_bp.route("/eliminar/<materia_id>", methods=["POST"])
def eliminar_materia(materia_id):
    parsed_id = limpiar_texto(materia_id)
    if not parsed_id:
        flash("Registro no encontrado", "warning")
        return redirect(url_for("materias.materias"))

    ok, err = delete_materia(parsed_id)
    if ok:
        flash("Materia eliminada", "success")
    else:
        flash(err or "Registro no encontrado", "danger")
    return redirect(url_for("materias.materias"))
