from flask import Flask, render_template, request, url_for, redirect, flash
from datetime import datetime
import db
from models import Tarea

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'

@app.route("/")
def home():
    todas_las_tareas = db.session.query(Tarea).all()
    categorias_unicas = {tarea.categoria for tarea in todas_las_tareas if tarea.categoria}
    return render_template("index.html", lista_de_tareas=todas_las_tareas, categorias_unicas=categorias_unicas)

@app.route("/filtrar", methods=["GET"])
def filtrar():
    categoria = request.args.get("categoria")
    if categoria:
        tareas_filtradas = db.session.query(Tarea).filter_by(categoria=categoria).all()
    else:
        tareas_filtradas = db.session.query(Tarea).all()
    categorias_unicas = {tarea.categoria for tarea in db.session.query(Tarea).all() if tarea.categoria}
    return render_template("index.html", lista_de_tareas=tareas_filtradas, categorias_unicas=categorias_unicas)

@app.route("/crear-tarea", methods=["POST"])
def crear():
    fecha_limite_str = request.form.get("fecha_limite")
    categoria = request.form.get("categoria")
    contenido_tarea = request.form.get("contenido_tarea")

    if not contenido_tarea or not categoria:
        flash("Por favor, introduce todos los campos.", "error")
        return redirect(url_for("home"))

    if fecha_limite_str:
        fecha_limite = datetime.strptime(fecha_limite_str, "%Y-%m-%d").date()
    else:
        fecha_limite = None

    tarea = Tarea(
        contenido=contenido_tarea,
        hecha=False,
        fecha_limite=fecha_limite,
        categoria=categoria
    )

    db.session.add(tarea)
    db.session.commit()
    return redirect(url_for("home"))

@app.route('/tarea-hecha/<id>')
def hecha(id):
    tarea = db.session.query(Tarea).filter_by(id=int(id)).first()
    tarea.hecha = not tarea.hecha
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/eliminar-tarea/<id>')
def eliminar(id):
    db.session.query(Tarea).filter_by(id=int(id)).delete()
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/editar-tarea/<id>', methods=["GET", "POST"])
def editar(id):
    tarea = db.session.query(Tarea).filter_by(id=int(id)).first()

    if request.method == "POST":
        tarea.contenido = request.form["contenido_tarea"]
        tarea.categoria = request.form.get("categoria")

        fecha_limite_str = request.form.get("fecha_limite")
        if fecha_limite_str:
            tarea.fecha_limite = datetime.strptime(fecha_limite_str, "%Y-%m-%d").date()
        else:
            tarea.fecha_limite = None

        db.session.commit()
        return redirect(url_for("home"))

    return render_template("editarTarea.html", tarea=tarea)

if __name__ == "__main__":
    db.Base.metadata.create_all(db.engine)
    app.run(debug=True)
