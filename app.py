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
    message = u'Révision faite ajoutée, date de la révision : ' + dateRevisionBus + ', idRévision: '+ idRevision + ', idBus : ' + idBus
    flash(message, 'alert-success')
    return redirect('/fait/show')
@app.route('/fait/delete', methods=['GET'])
def delete_fait():
    idFait = request.args.get('id', '')
    bdd = get_db().cursor()
    sql = "DELETE FROM fait WHERE idFait = %s"
    bdd.execute(sql, idFait)
    get_db().commit()
    message = u'Révision faite supprimée, ID: ' + idFait
    flash(message, 'alert-danger')
    return redirect('/fait/show')
@app.route('/fait/edit', methods=['GET'])
def edit_fait():
    idFait = request.args.get('id', '')
    bdd1 = get_db().cursor()
    bdd2 = get_db().cursor()
    bdd3 = get_db().cursor()
    sql1 = """SELECT r.*
              FROM revision r"""
    sql2 = """SELECT f.*
             FROM fait f
             WHERE idFait = %s"""
    sql3 = """SELECT b.*
              FROM bus b"""
    bdd1.execute(sql1)
    bdd2.execute(sql2, (idFait))
    bdd3.execute(sql3)
    revision = bdd1.fetchall()
    fait = bdd2.fetchone()
    bus = bdd3.fetchall()
    return render_template('fait/edit_fait.html', revision=revision, fait=fait, bus=bus)
@app.route('/fait/edit', methods=['POST'])
def valid_edit_fait():
    bdd = get_db().cursor()
    idFait = request.form.get('id-Fait', '')
    dateRevisionBus = request.form.get('date-Revision', '')
    idRevision = request.form.get('id-Revision', '')
    idBus = request.form.get('id-Bus', '')
    sql = """UPDATE fait
             SET dateRevisionBus = %s,
                 idRevision = %s,
                 idBus = %s
                 WHERE idFait = %s"""
    bdd.execute(sql, [dateRevisionBus, idRevision, idBus, idFait])
    get_db().commit()
    message = u'Révision faite modifiée, date de la révision : ' + dateRevisionBus + ', Révision numéro : '+ idRevision + ', Bus : ' + idBus
    flash(message, 'alert-warning')
    return redirect('/fait/show')

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
    bdd1 = get_db().cursor()
    bdd2 = get_db().cursor()
    sql1 = """SELECT rev.*
              FROM revision rev"""
    sql2 = """SELECT res.*
              FROM reservoir res"""
    bdd1.execute(sql1)
    bdd2.execute(sql2)
    revision = bdd1.fetchall()
    reservoir = bdd2.fetchall()
    return render_template('recoit/add_recoit.html', revision=revision, reservoir=reservoir)
@app.route('/recoit/add', methods=['POST'])
def valid_add_recoit():
    dateRevisionReservoir = request.form.get('date-Revision', '')
    idRevision = request.form.get('id-Revision', '')
    idReservoir = request.form.get('id-Reservoir', '')
    bdd = get_db().cursor()
    sql = """INSERT INTO recoit (
              dateRevisionReservoir,
              idRevision,
              idReservoir)
              VALUES (%s, %s, %s)"""
    bdd.execute(sql,(dateRevisionReservoir, idRevision, idReservoir))
    get_db().commit()
    message = u'Révision reçue ajoutée, date de la révision : ' + dateRevisionReservoir + ', idRévision: '+ idRevision + ', idReservoir : ' + idReservoir
    flash(message, 'alert-success')
    return redirect('/recoit/show')
@app.route('/recoit/delete', methods=['GET'])
def delete_recoit():
    idRecoit = request.args.get('id', '')
    bdd = get_db().cursor()
    sql = "DELETE FROM recoit WHERE idRecoit = %s"
    bdd.execute(sql, idRecoit)
    get_db().commit()
    message = u'Révision reçue supprimée, ID: ' + idRecoit
    flash(message, 'alert-danger')
    return redirect('/recoit/show')
@app.route('/recoit/edit', methods=['GET'])
def edit_recoit():
    idRecoit = request.args.get('id', '')
    bdd1 = get_db().cursor()
    bdd2 = get_db().cursor()
    bdd3 = get_db().cursor()
    sql1 = """SELECT rev.*
              FROM revision rev"""
    sql2 = """SELECT rec.*
             FROM recoit rec
             WHERE idRecoit = %s"""
    sql3 = """SELECT res.*
              FROM reservoir res"""
    bdd1.execute(sql1)
    bdd2.execute(sql2, [idRecoit])
    bdd3.execute(sql3)
    revision = bdd1.fetchall()
    recoit = bdd2.fetchone()
    reservoir = bdd3.fetchall()
    return render_template('recoit/edit_recoit.html', revision=revision, recoit=recoit, reservoir=reservoir)
@app.route('/recoit/edit', methods=['POST'])
def valid_edit_recoit():
    bdd = get_db().cursor()
    idRecoit = request.form.get('id-Recoit', '')
    dateRevisionReservoir = request.form.get('date-Revision', '')
    idRevision = request.form.get('id-Revision', '')
    idReservoir = request.form.get('id-Reservoir', '')
    sql = """UPDATE recoit
             SET dateRevisionReservoir = %s,
                 idRevision = %s,
                 idReservoir = %s
                 WHERE idRecoit = %s"""
    bdd.execute(sql, [dateRevisionReservoir, idRevision, idReservoir, idRecoit])
    get_db().commit()
    message = u'Révision reçue modifiée, date de la révision : ' + dateRevisionReservoir + ', Révision numéro : '+ idRevision + ', Réservoir numéro : : ' + idReservoir
    flash(message, 'alert-warning')
    return redirect('/recoit/show')

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
    bdd1 = get_db().cursor()
    bdd2 = get_db().cursor()
    sql1 = """SELECT a.*
              FROM anneeConsommation a"""
    sql2 = """SELECT b.*
              FROM bus b"""
    bdd1.execute(sql1)
    bdd2.execute(sql2)
    anneeConsommation = bdd1.fetchall()
    bus = bdd2.fetchall()
    return render_template('consommation/add_consommation.html', anneeConsommation=anneeConsommation, bus=bus)
@app.route('/consommation/add', methods=['POST'])
def valid_add_consommation():
    nbconsommation = request.form.get('nbconsommation', '')
    distance = request.form.get('distance', '')
    anneeConsommation = request.form.get('anneeConsommation', '')
    idBus = request.form.get('id-Bus', '')
    bdd = get_db().cursor()
    sql = """INSERT INTO consommation (
              nbconsommation,
              distance,
              annee,
              idBus)
              VALUES (%s, %s, %s, %s)"""
    bdd.execute(sql,(nbconsommation, distance, anneeConsommation, idBus))
    get_db().commit()
    message = u'Consommation ajoutée, consommation : ' + nbconsommation + ', distance : '+ distance + ', annee : ' + anneeConsommation + ', idBus : ' + idBus
    flash(message, 'alert-success')
    return redirect('/consommation/show')
@app.route('/consommation/delete', methods=['GET'])
def delete_consommation():
    idConsommation = request.args.get('id', '')
    bdd = get_db().cursor()
    sql = "DELETE FROM consommation WHERE idConsommation = %s"
    bdd.execute(sql, idConsommation)
    get_db().commit()
    message = u'Consommation supprimée, ID: ' + idConsommation
    flash(message, 'alert-danger')
    return redirect('/consommation/show')
@app.route('/consommation/edit', methods=['GET'])
def edit_consommation():
    idConsommation = request.args.get('id', '')
    bdd1 = get_db().cursor()
    bdd2 = get_db().cursor()
    bdd3 = get_db().cursor()
    sql1 = """SELECT a.*
              FROM anneeConsommation a"""
    sql2 = """SELECT c.*
              FROM consommation c
              WHERE idConsommation = %s"""
    sql3 = """SELECT b.*
              FROM bus b"""
    bdd1.execute(sql1)
    bdd2.execute(sql2, [idConsommation])
    bdd3.execute(sql3)
    anneeConsommation = bdd1.fetchall()
    consommation = bdd2.fetchone()
    bus = bdd3.fetchall()
    return render_template('consommation/edit_consommation.html', anneeConsommation=anneeConsommation, consommation=consommation, bus=bus)
@app.route('/consommation/edit', methods=['POST'])
def valid_edit_consommation():
    bdd = get_db().cursor()
    idConsommation = request.form.get('id-Consommation', '')
    nbconsommation = request.form.get('nbconsommation', '')
    distance = request.form.get('distance', '')
    anneeConsommation = request.form.get('anneeConsommation', '')
    idBus = request.form.get('id-Bus', '')
    sql = """UPDATE consommation
             SET nbconsommation = %s,
                 distance = %s,
                 annee = %s,
                 idBus = %s
                 WHERE idConsommation = %s"""
    bdd.execute(sql, [nbconsommation, distance, anneeConsommation, idBus, idConsommation])
    get_db().commit()
    message = u'Consommation modifiée, consomme : ' + nbconsommation + ', distance : ' + distance + ', annee : ' + anneeConsommation + ', Bus : ' + idBus
    flash(message, 'alert-warning')
    return redirect('/consommation/show')


if __name__ == '__main__':
    app.run()
