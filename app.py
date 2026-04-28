from flask import Flask

from routes.alumnos import alumnos_bp
from routes.asignaciones import asignaciones_bp
from routes.calificaciones import calificaciones_bp
from routes.docentes import docentes_bp
from routes.home import home_bp
from routes.materias import materias_bp
from routes.reportes import reportes_bp

app = Flask(__name__)
app.secret_key = "SCA"

app.register_blueprint(home_bp)
app.register_blueprint(alumnos_bp, url_prefix="/alumnos")
app.register_blueprint(docentes_bp, url_prefix="/docentes")
app.register_blueprint(materias_bp, url_prefix="/materias")
app.register_blueprint(asignaciones_bp, url_prefix="/asignaciones")
app.register_blueprint(calificaciones_bp, url_prefix="/calificaciones")
app.register_blueprint(reportes_bp, url_prefix="/reportes")


if __name__ == "__main__":
    app.run(debug=True)