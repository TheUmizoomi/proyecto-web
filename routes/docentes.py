from flask import Blueprint, flash, redirect, render_template, request, url_for

from models.docentes_model import (
    create_docente,
    delete_docente,
    get_docente,
    list_docentes,
    update_docente,
)
from routes.validators import clean_text, validar_correo, validar_solo_numeros, validar_solo_texto

docentes_bp = Blueprint("docentes", __name__)


def _render_docentes(open_modal=None, draft=None):
    return render_template(
        "docentes.html",
        docentes=list_docentes(),
        open_modal=open_modal,
        draft=draft or {},
    )


@docentes_bp.route("/", methods=["GET", "POST"])
def docentes():
    if request.method == "POST":
        nombre = clean_text(request.form.get("nombre"))
        paterno = clean_text(request.form.get("apellido_paterno") or request.form.get("paterno"))
        materno = clean_text(request.form.get("apellido_materno") or request.form.get("materno"))
        correo = clean_text(request.form.get("correo"))
        telefono = clean_text(request.form.get("telefono"))
        grado_academico = _normalizar_grado_academico(request.form.get("grado_academico"))

        draft = {
            "nombre": nombre,
            "apellido_paterno": paterno,
            "apellido_materno": materno,
            "correo": correo,
            "telefono": telefono,
            "grado_academico": grado_academico,
        }
        if not nombre or not validar_solo_texto(nombre):
            flash("Nombre invalido", "danger")
            return _render_docentes(open_modal="modalNuevoDocente", draft=draft)
        if not paterno or not validar_solo_texto(paterno):
            flash("Apellido paterno invalido", "danger")
            return _render_docentes(open_modal="modalNuevoDocente", draft=draft)
        if not materno or not validar_solo_texto(materno):
            flash("Apellido materno invalido", "danger")
            return _render_docentes(open_modal="modalNuevoDocente", draft=draft)
        if not correo or not validar_correo(correo):
            flash("Correo invalido", "danger")
            return _render_docentes(open_modal="modalNuevoDocente", draft=draft)
        if not telefono or not validar_solo_numeros(telefono):
            flash("Telefono invalido", "danger")
            return _render_docentes(open_modal="modalNuevoDocente", draft=draft)
        if not grado_academico or not validar_solo_texto(grado_academico):
            flash("Grado academico invalido", "danger")
            return _render_docentes(open_modal="modalNuevoDocente", draft=draft)

        ok, err = create_docente(nombre, paterno, materno, correo, telefono, grado_academico)
        if ok:
            flash("Docente registrado correctamente", "success")
            return redirect(url_for("docentes.docentes"))
        flash("Operacion no permitida" if err else "Datos invalidos", "danger")

    return _render_docentes()


def _normalizar_grado_academico(valor: str) -> str:
    v = clean_text(valor)
    if not v:
        return ""
    lower = v.lower()
    if lower in {"doctor", "dr", "dr.", "doctorado"}:
        return "Doctorado"
    return v


@docentes_bp.route("/editar/<docente_id>", methods=["POST"])
def editar_docente(docente_id):
    parsed_id = clean_text(docente_id)
    if not parsed_id:
        flash("Registro no encontrado", "warning")
        return redirect(url_for("docentes.docentes"))

    docente = get_docente(parsed_id)
    if not docente:
        flash("Registro no encontrado", "warning")
        return redirect(url_for("docentes.docentes"))

    nombre = clean_text(request.form.get("nombre"))
    paterno = clean_text(request.form.get("apellido_paterno") or request.form.get("paterno"))
    materno = clean_text(request.form.get("apellido_materno") or request.form.get("materno"))
    correo = clean_text(request.form.get("correo"))
    telefono = clean_text(request.form.get("telefono"))
    grado_academico = _normalizar_grado_academico(request.form.get("grado_academico"))
    modal_id = f"modalEditarDocente{parsed_id}"
    draft = {
        "nombre": nombre,
        "apellido_paterno": paterno,
        "apellido_materno": materno,
        "correo": correo,
        "telefono": telefono,
        "grado_academico": grado_academico,
    }

    if not nombre or not validar_solo_texto(nombre):
        flash("Nombre invalido", "danger")
        return _render_docentes(open_modal=modal_id, draft=draft)
    if not paterno or not validar_solo_texto(paterno):
        flash("Apellido paterno invalido", "danger")
        return _render_docentes(open_modal=modal_id, draft=draft)
    if not materno or not validar_solo_texto(materno):
        flash("Apellido materno invalido", "danger")
        return _render_docentes(open_modal=modal_id, draft=draft)
    if not correo or not validar_correo(correo):
        flash("Correo invalido", "danger")
        return _render_docentes(open_modal=modal_id, draft=draft)
    if not telefono or not validar_solo_numeros(telefono):
        flash("Telefono invalido", "danger")
        return _render_docentes(open_modal=modal_id, draft=draft)
    if not grado_academico or not validar_solo_texto(grado_academico):
        flash("Grado academico invalido", "danger")
        return _render_docentes(open_modal=modal_id, draft=draft)

    ok, err = update_docente(parsed_id, nombre, paterno, materno, correo, telefono, grado_academico)
    if ok:
        flash("Docente actualizado", "success")
    else:
        flash(err or "Operacion no permitida", "danger")
    return redirect(url_for("docentes.docentes"))


@docentes_bp.route("/eliminar/<docente_id>", methods=["POST"])
def eliminar_docente(docente_id):
    parsed_id = clean_text(docente_id)
    if not parsed_id:
        flash("Registro no encontrado", "warning")
        return redirect(url_for("docentes.docentes"))

    ok, err = delete_docente(parsed_id)
    if ok:
        flash("Docente eliminado", "success")
    else:
        flash(err or "Registro no encontrado", "danger")
    return redirect(url_for("docentes.docentes"))
