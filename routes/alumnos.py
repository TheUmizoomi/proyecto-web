from flask import Blueprint, flash, redirect, render_template, request, url_for

from models.alumnos_model import (
    create_alumno,
    delete_alumno,
    get_detalle_alumno,
    get_alumno,
    list_alumnos,
    update_alumno,
)
from models.calificaciones_model import (
    get_calificaciones_por_alumno,
    save_calificaciones_por_alumno,
)
from models.materias_model import list_materias
from routes.validators import (
    clean_text,
    limpiar_texto,
    obtener_periodo_actual,
    validar_solo_numeros,
    validar_solo_texto,
)

alumnos_bp = Blueprint("alumnos", __name__)


def _parse_edad(value):
    try:
        edad = int(value)
    except (TypeError, ValueError):
        return None
    return edad if 16 <= edad <= 25 else None


def _parse_calificacion(value):
    try:
        calificacion = float(value)
    except (TypeError, ValueError):
        return None
    return calificacion if 0 <= calificacion <= 100 else None


@alumnos_bp.route("/", methods=["GET", "POST"])
def alumnos():
    query = clean_text(request.args.get("q"))

    if request.method == "POST":
        matricula = limpiar_texto(request.form.get("matricula"))
        nombre = limpiar_texto(request.form.get("nombre"))
        apellido_paterno = limpiar_texto(request.form.get("apellido_paterno"))
        apellido_materno = limpiar_texto(request.form.get("apellido_materno"))
        carrera = limpiar_texto(request.form.get("carrera")).upper()
        sexo = limpiar_texto(request.form.get("sexo"))
        telefono = limpiar_texto(request.form.get("telefono"))
        edad = _parse_edad(request.form.get("edad"))

        if (
            not matricula
            or not nombre
            or not apellido_paterno
            or not apellido_materno
            or not carrera
            or not telefono
            or sexo not in {"Masculino", "Femenino", "Otro"}
            or not validar_solo_texto(nombre)
            or not validar_solo_texto(apellido_paterno)
            or not validar_solo_texto(apellido_materno)
            or not validar_solo_numeros(telefono)
            or edad is None
        ):
            flash("Datos inválidos", "danger")
        else:
            ok, err = create_alumno(
                matricula,
                nombre,
                apellido_paterno,
                apellido_materno,
                carrera,
                sexo,
                edad,
                telefono,
            )
            if ok:
                flash("Alumno registrado correctamente", "success")
                return redirect(url_for("alumnos.alumnos"))
            flash("Operación no permitida" if err else "Datos inválidos", "danger")

    alumnos_data = list_alumnos()
    if query:
        low = query.lower()
        alumnos_data = [
            alumno
            for alumno in alumnos_data
            if low in (alumno.get("matricula") or "").lower()
            or low in (alumno.get("nombre") or "").lower()
            or low in (alumno.get("apellido_paterno") or "").lower()
            or low in (alumno.get("apellido_materno") or "").lower()
            or low in (alumno.get("carrera") or "").lower()
        ]

    return render_template(
        "alumnos.html",
        alumnos=alumnos_data,
        query=query,
        open_modal=None,
        draft={},
    )


@alumnos_bp.route("/editar/<alumno_id>", methods=["GET", "POST"])
def editar_alumno(alumno_id):
    parsed_id = clean_text(alumno_id)
    if not parsed_id:
        flash("Registro no encontrado", "warning")
        return redirect(url_for("alumnos.alumnos"))

    alumno = get_alumno(parsed_id)
    if not alumno:
        flash("Registro no encontrado", "warning")
        return redirect(url_for("alumnos.alumnos"))

    if request.method == "POST":
        matricula = limpiar_texto(request.form.get("matricula"))
        nombre = limpiar_texto(request.form.get("nombre"))
        apellido_paterno = limpiar_texto(request.form.get("apellido_paterno"))
        apellido_materno = limpiar_texto(request.form.get("apellido_materno"))
        carrera = limpiar_texto(request.form.get("carrera")).upper()
        sexo = limpiar_texto(request.form.get("sexo"))
        telefono = limpiar_texto(request.form.get("telefono"))
        edad = _parse_edad(request.form.get("edad"))
        if (
            not matricula
            or not nombre
            or not apellido_paterno
            or not apellido_materno
            or not carrera
            or not telefono
            or sexo not in {"Masculino", "Femenino", "Otro"}
            or not validar_solo_texto(nombre)
            or not validar_solo_texto(apellido_paterno)
            or not validar_solo_texto(apellido_materno)
            or not validar_solo_numeros(telefono)
            or edad is None
        ):
            flash("Datos inválidos", "danger")
        else:
            ok, err = update_alumno(
                parsed_id,
                matricula,
                nombre,
                apellido_paterno,
                apellido_materno,
                carrera,
                sexo,
                edad,
                telefono,
            )
            if ok:
                flash("Alumno actualizado", "success")
                return redirect(url_for("alumnos.alumnos"))
            flash("Operación no permitida" if err else "Datos inválidos", "danger")

    return redirect(url_for("alumnos.alumnos"))


@alumnos_bp.route("/eliminar/<alumno_id>", methods=["POST"])
def eliminar_alumno(alumno_id):
    parsed_id = clean_text(alumno_id)
    if not parsed_id:
        flash("Registro no encontrado", "warning")
        return redirect(url_for("alumnos.alumnos"))

    ok, err = delete_alumno(parsed_id)
    if ok:
        flash("Alumno eliminado", "success")
    else:
        flash(err or "Registro no encontrado", "danger")
    return redirect(url_for("alumnos.alumnos"))


@alumnos_bp.route("/ver/<alumno_id>", methods=["GET"])
def ver_alumno(alumno_id):
    parsed_id = clean_text(alumno_id)
    if not parsed_id:
        flash("Registro no encontrado", "warning")
        return redirect(url_for("alumnos.alumnos"))

    alumno = get_alumno(parsed_id)
    if not alumno:
        flash("Registro no encontrado", "warning")
        return redirect(url_for("alumnos.alumnos"))

    detalle = get_detalle_alumno(parsed_id)
    return render_template("alumno_ver.html", alumno=alumno, detalle=detalle)


@alumnos_bp.route("/calificaciones/<alumno_id>", methods=["GET", "POST"])
def calificaciones_alumno(alumno_id):
    parsed_id = clean_text(alumno_id)
    if not parsed_id:
        flash("Registro no encontrado", "warning")
        return redirect(url_for("alumnos.alumnos"))

    alumno = get_alumno(parsed_id)
    if not alumno:
        flash("Registro no encontrado", "warning")
        return redirect(url_for("alumnos.alumnos"))

    materias = list_materias()
    existentes = get_calificaciones_por_alumno(parsed_id)
    calificaciones_map = {item.get("materia_id"): item for item in existentes}
    materias_disponibles = [m for m in materias if m.get("id") not in calificaciones_map]

    if request.method == "POST":
        lista_calificaciones = []
        # Editar calificaciones existentes.
        for item in existentes:
            materia_id = item.get("materia_id")
            if not materia_id:
                continue
            calificacion_raw = clean_text(request.form.get(f"calificacion_{materia_id}"))
            periodo = obtener_periodo_actual()
            if not calificacion_raw and not periodo:
                continue
            calificacion = _parse_calificacion(calificacion_raw)
            if calificacion is None:
                flash("Datos inválidos en calificaciones existentes", "danger")
                return redirect(url_for("alumnos.calificaciones_alumno", alumno_id=parsed_id))
            lista_calificaciones.append(
                {"materia_id": materia_id, "calificacion": calificacion, "periodo": periodo}
            )

        # Agregar nueva calificacion de una materia.
        nueva_materia_id = clean_text(request.form.get("nueva_materia_id"))
        nueva_calificacion_raw = clean_text(request.form.get("nueva_calificacion"))
        nuevo_periodo = obtener_periodo_actual()
        if nueva_materia_id or nueva_calificacion_raw:
            nueva_calificacion = _parse_calificacion(nueva_calificacion_raw)
            if not nueva_materia_id or nueva_calificacion is None:
                flash("Completa materia y calificación para agregar una nueva", "danger")
                return redirect(url_for("alumnos.calificaciones_alumno", alumno_id=parsed_id))
            lista_calificaciones.append(
                {
                    "materia_id": nueva_materia_id,
                    "calificacion": nueva_calificacion,
                    "periodo": nuevo_periodo,
                }
            )

        if not lista_calificaciones:
            flash("No hay cambios para guardar", "warning")
            return redirect(url_for("alumnos.calificaciones_alumno", alumno_id=parsed_id))

        ok, err = save_calificaciones_por_alumno(parsed_id, lista_calificaciones)
        if ok:
            flash("Calificaciones guardadas correctamente", "success")
        else:
            flash(err or "No se pudieron guardar las calificaciones", "danger")
        return redirect(url_for("alumnos.calificaciones_alumno", alumno_id=parsed_id))

    return render_template(
        "calificaciones_alumno.html",
        alumno=alumno,
        existentes=existentes,
        materias_disponibles=materias_disponibles,
        periodo_actual=obtener_periodo_actual(),
    )
