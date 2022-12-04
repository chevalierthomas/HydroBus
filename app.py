#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Flask, request, render_template, redirect, url_for, abort, flash

app = Flask(__name__)
app.secret_key = 'une cle(token) : grain de sel(any random string)'

## à ajouter
from flask import session, g
import pymysql.cursors

def get_db():
    if 'db' not in g:
        g.db = pymysql.connect(
            host="localhost",  # à modifier
            user="mnotter",  # à modifier
            password="1504",  # à modifier
            database="BDD_mnotter",  # à modifier
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
    return g.db

@app.teardown_appcontext
def teardown_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

@app.route('/')
def show_accueil():
    return render_template('layout.html')

@app.route('/reservoir/show')
def show_reservoir():
    bdd = get_db().cursor()
    sql = """SELECT r.*, m.idModele, idB.idBus
             FROM reservoir r
             LEFT JOIN modele m ON r.idModele = m.idModele
             LEFT JOIN bus idB ON r.idBus = idB.idBus
             ORDER BY r.idReservoir"""
    bdd.execute(sql)
    reservoir = bdd.fetchall()
    return render_template('reservoir/show_reservoir.html', reservoir=reservoir)
@app.route('/reservoir/add', methods=['GET'])
def add_reservoir():
    bdd1 = get_db().cursor()
    bdd2 = get_db().cursor()
    sql1 = """SELECT m.*
              FROM modele m"""
    sql2 = """SELECT b.*
              FROM bus b"""
    bdd1.execute(sql1)
    bdd2.execute(sql2)
    modele = bdd1.fetchall()
    bus = bdd2.fetchall()
    return render_template('reservoir/add_reservoir.html', modele=modele, bus=bus)
@app.route('/reservoir/add', methods=['POST'])
def valid_add_reservoir():
    idModele = request.form.get('id-Modele', '')
    idBus = request.form.get('id-Bus', '')
    bdd = get_db().cursor()
    sql = """INSERT INTO reservoir (
              idModele,
              idBus)
              VALUES (%s, %s)"""
    bdd.execute(sql,(idModele, idBus))
    get_db().commit()
    message = u'Réservoir ajouté, idModèle: '+ idModele + ', idBus : ' + idBus
    flash(message, 'alert-success')
    return redirect('/reservoir/show')
@app.route('/reservoir/delete', methods=['GET'])
def delete_reservoir():
    idReservoir = request.args.get('id', '')
    bdd = get_db().cursor()
    sql = "DELETE FROM reservoir WHERE idReservoir = %s"
    bdd.execute(sql, idReservoir)
    get_db().commit()
    message = u'Réservoir supprimé, ID: ' + idReservoir
    flash(message, 'alert-danger')
    return redirect('/reservoir/show')
@app.route('/reservoir/edit', methods=['GET'])
def edit_reservoir():
    idReservoir = request.args.get('id', '')
    bdd1 = get_db().cursor()
    bdd2 = get_db().cursor()
    bdd3 = get_db().cursor()
    sql1 = """SELECT m.*
              FROM modele m"""
    sql2 = """SELECT r.*
             FROM reservoir r
             WHERE idReservoir = %s"""
    sql3 = """SELECT bus.*
              FROM bus"""
    bdd1.execute(sql1)
    bdd2.execute(sql2, (idReservoir))
    bdd3.execute(sql3)
    modele = bdd1.fetchall()
    reservoir = bdd2.fetchone()
    bus = bdd3.fetchall()
    return render_template('reservoir/edit_reservoir.html', modele=modele, reservoir=reservoir, bus=bus)
@app.route('/reservoir/edit', methods=['POST'])
def valid_edit_reservoir():
    bdd = get_db().cursor()
    idReservoir = request.form.get('id-Reservoir', '')
    idModele = request.form.get('id-Modele', '')
    idBus = request.form.get('id-Bus', '')
    sql = """UPDATE reservoir
             SET idModele = %s,
                 idBus = %s
                 WHERE idReservoir = %s"""
    bdd.execute(sql, [idModele, idBus, idReservoir])
    get_db().commit()
    message = u'Réservoir modifié, ID: ' + idReservoir + ', Modele: ' + idModele + ', Bus : ' + idBus
    flash(message, 'alert-warning')
    return redirect('/reservoir/show')

@app.route('/fait/show')
def show_fait():
    bdd = get_db().cursor()
    sql = """SELECT f.*, idR.idRevision, idB.idBus
             FROM fait f
             LEFT JOIN revision idR ON f.idRevision = idR.idRevision
             LEFT JOIN bus idB ON f.idBus = idB.idBus
             ORDER BY f.idFait"""
    bdd.execute(sql)
    fait = bdd.fetchall()
    return render_template('fait/show_fait.html', fait=fait)
@app.route('/fait/add', methods=['GET'])
def add_fait():
    bdd1 = get_db().cursor()
    bdd2 = get_db().cursor()
    sql1 = """SELECT r.*
              FROM revision r"""
    sql2 = """SELECT b.*
              FROM bus b"""
    bdd1.execute(sql1)
    bdd2.execute(sql2)
    revision = bdd1.fetchall()
    bus = bdd2.fetchall()
    return render_template('fait/add_fait.html', revision=revision, bus=bus)
@app.route('/fait/add', methods=['POST'])
def valid_add_fait():
    dateRevisionBus = request.form.get('date-Revision', '')
    idRevision = request.form.get('id-Revision', '')
    idBus = request.form.get('id-Bus', '')
    bdd = get_db().cursor()
    sql = """INSERT INTO fait (
              dateRevisionBus,
              idRevision,
              idBus)
              VALUES (%s, %s, %s)"""
    bdd.execute(sql,(dateRevisionBus, idRevision, idBus))
    get_db().commit()
    message = u'Révision faite ajouté, date de la révision : ' + dateRevisionBus + ', idRévision: '+ idRevision + ', idBus : ' + idBus
    flash(message, 'alert-success')
    return redirect('/fait/show')
@app.route('/fait/delete', methods=['GET'])
def delete_fait():
    return redirect('/fait/show')

@app.route('/fait/edit', methods=['GET'])
def edit_fait():
    return render_template('fait/edit_fait.html')
@app.route('/fait/edit', methods=['POST'])
def valid_edit_fait():
    return redirect('/fait/show')

@app.route('/consommation/show')
def show_consommation():
    bdd = get_db().cursor()
    sql = """SELECT c.*, a.annee, idB.idBus
             FROM consommation c
             LEFT JOIN anneeConsommation a ON c.annee = a.annee
             LEFT JOIN bus idB ON c.idBus = idB.idBus
             ORDER BY c.idConsommation"""
    bdd.execute(sql)
    consommation = bdd.fetchall()
    return render_template('consommation/show_consommation.html', consommation=consommation)
@app.route('/consommation/add', methods=['GET'])
def add_consommation():
    return render_template('consommation/add_consommation.html')
@app.route('/consommation/add', methods=['POST'])
def valid_add_consommation():
    return redirect('/consommation/show')
@app.route('/consommation/delete', methods=['GET'])
def delete_consommation():
    return redirect('/consommation/show')
@app.route('/consommation/delete', methods=['POST'])
def valid_delete_consommation():
    return redirect('/consommation/show')
@app.route('/consommation/edit', methods=['GET'])
def edit_consommation():
    return render_template('consommation/edit_consommation.html')
@app.route('/consommation/edit', methods=['POST'])
def valid_edit_consommation():
    return redirect('/consommation/show')

@app.route('/recoit/show')
def show_recoit():
    bdd = get_db().cursor()
    sql = """SELECT r.*, idRev.idRevision, idRes.idReservoir
             FROM recoit r
             LEFT JOIN revision idRev ON r.idRevision = idRev.idRevision
             LEFT JOIN reservoir idRes ON r.idReservoir = idRes.idReservoir
             ORDER BY r.idRecoit"""
    bdd.execute(sql)
    recoit = bdd.fetchall()
    return render_template('recoit/show_recoit.html', recoit=recoit)
@app.route('/recoit/add', methods=['GET'])
def add_recoit():
    return render_template('recoit/add_recoit.html')
@app.route('/recoit/add', methods=['POST'])
def valid_add_recoit():
    return redirect('/recoit/show')
@app.route('/recoit/delete', methods=['GET'])
def delete_recoit():
    return redirect('/recoit/show')
@app.route('/recoit/delete', methods=['POST'])
def valid_delete_recoit():
    return redirect('/recoit/show')
@app.route('/recoit/edit', methods=['GET'])
def edit_recoit():
    return render_template('recoit/edit_recoit.html')
@app.route('/recoit/edit', methods=['POST'])
def valid_edit_recoit():
    return redirect('/recoit/show')


if __name__ == '__main__':
    app.run()
