from flask import Blueprint, flash, render_template, request

from models.alumnos_model import list_alumnos
from models.reportes_model import reporte_general, reporte_por_alumno
from routes.validators import clean_text

reportes_bp = Blueprint("reportes", __name__)


@reportes_bp.route("/", methods=["GET"])
def reportes():
    alumno_id = clean_text(request.args.get("alumno_id"))
    reporte_alumno = None

    if request.args.get("alumno_id"):
        if not alumno_id:
            flash("Datos inválidos", "danger")
        else:
            reporte_alumno = reporte_por_alumno(alumno_id)
            if not reporte_alumno:
                flash("Registro no encontrado", "warning")

    return render_template(
        "reportes.html",
        alumnos=list_alumnos(),
        reporte_alumno=reporte_alumno,
        reporte_general=reporte_general(),
        selected_alumno=alumno_id,
    )
