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


@app.route('/bus/show')
def show_bus():
    bdd = get_db().cursor()
    sql = """SELECT b.*
             FROM bus b
             ORDER BY b.idBus"""
    bdd.execute(sql)
    bus = bdd.fetchall()
    return render_template('bus/show_bus.html', bus=bus)
@app.route('/bus/etat', methods=['GET'])
def etat_bus():
    idBus = request.args.get('id', '')
    bdd1 = get_db().cursor()
    bdd2 = get_db().cursor()
    bdd3 = get_db().cursor()
    bdd4 = get_db().cursor()
    bdd5 = get_db().cursor()
    sql1 = """SELECT b.*, COUNT(a.idBus) AS nb_accident
             FROM bus b
             LEFT JOIN accident a ON b.idBus = a.idBus
             WHERE b.idBus = %s"""
    sql2 = """SELECT b.*, MAX(c.nbconsommation) AS max_consommation
              FROM bus b
              LEFT JOIN consommation c ON b.idBus = c.idBus
              WHERE b.idBus = %s"""
    sql3 = """SELECT b.*, COUNT(f.idBus) AS nb_revision
             FROM bus b
             LEFT JOIN fait f ON b.idBus = f.idBus
             WHERE b.idBus = %s"""
    sql4 = """SELECT b.*, MAX(f.dateRevisionBus) AS revision_recente
             FROM bus b
             LEFT JOIN fait f ON b.idBus = f.idBus
             WHERE b.idBus = %s"""
    sql5 = """SELECT b.*, SUM(c.distance) AS somme_distance
             FROM bus b
             LEFT JOIN consommation c ON b.idBus = c.idBus
             WHERE b.idBus = %s"""
    bdd1.execute(sql1, [idBus])
    bdd2.execute(sql2, [idBus])
    bdd3.execute(sql3, [idBus])
    bdd4.execute(sql4, [idBus])
    bdd5.execute(sql5, [idBus])
    bus = bdd1.fetchone()
    bus2 = bdd2.fetchone()
    bus3 = bdd3.fetchone()
    bus4 = bdd4.fetchone()
    bus5 = bdd5.fetchone()
    return render_template('bus/etat_bus.html', bus=bus, bus2=bus2, bus3=bus3, bus4=bus4, bus5=bus5)
@app.route('/bus/valid_etat', methods=['POST'])
def valid_etat_bus():
    return redirect('/bus/show')
@app.route('/bus/add', methods=['GET'])
def add_bus():
    bdd = get_db().cursor()
    sql = """SELECT b.*
              FROM bus b"""
    bdd.execute(sql)
    bus = bdd.fetchall()
    return render_template('bus/add_bus.html', bus=bus)
@app.route('/bus/add', methods=['POST'])
def valid_add_bus():
    dateAchat = request.form.get('date-achat', '')
    bdd = get_db().cursor()
    sql = """INSERT INTO bus (
              dateAchat)
              VALUES (%s)"""
    bdd.execute(sql,(dateAchat))
    get_db().commit()
    message = u'Bus ajouté, Date d-achat : '+ dateAchat
    flash(message, 'alert-success')
    return redirect('/bus/show')
@app.route('/bus/delete', methods=['GET'])
def delete_bus():
    idBus = request.args.get('id', '')
    bdd = get_db().cursor()
    sql = "DELETE FROM bus WHERE idBus = %s"
    bdd.execute(sql, idBus)
    get_db().commit()
    message = u'Bus supprimé, ID: ' + idBus
    flash(message, 'alert-danger')
    return redirect('/bus/show')
@app.route('/bus/edit', methods=['GET'])
def edit_bus():
    idBus = request.args.get('id', '')
    bdd = get_db().cursor()
    sql = """SELECT b.*
             FROM bus b
             WHERE idBus = %s"""
    bdd.execute(sql, (idBus))
    bus = bdd.fetchone()
    return render_template('bus/edit_bus.html', bus=bus)
@app.route('/bus/edit', methods=['POST'])
def valid_edit_bus():
    bdd = get_db().cursor()
    idBus = request.form.get('id-Bus', '')
    dateAchat = request.form.get('date-achat', '')
    sql = """UPDATE bus
             SET dateAchat = %s
             WHERE idBus = %s"""
    bdd.execute(sql, [dateAchat, idBus])
    get_db().commit()
    message = u'Bus modifié, ID: ' + idBus + ', date d-achat : ' + dateAchat
    flash(message, 'alert-warning')
    return redirect('/bus/show')


@app.route('/revision/show')
def show_revision():
    bdd = get_db().cursor()
    sql = """SELECT r.*
             FROM revision r
             ORDER BY r.idRevision"""
    bdd.execute(sql)
    revision = bdd.fetchall()
    return render_template('revision/show_revision.html', revision=revision)
@app.route('/revision/add', methods=['GET'])
def add_revision():
    bdd = get_db().cursor()
    sql = """SELECT r.*
              FROM revision r"""
    bdd.execute(sql)
    revision = bdd.fetchall()
    return render_template('revision/add_revision.html', revision=revision)
@app.route('/revision/add', methods=['POST'])
def valid_add_revision():
    observation = request.form.get('observation', '')
    bdd = get_db().cursor()
    sql = """INSERT INTO revision (
              observation)
              VALUES (%s)"""
    bdd.execute(sql,(observation))
    get_db().commit()
    message = u'Révision ajouté, Observation : '+ observation
    flash(message, 'alert-success')
    return redirect('/revision/show')
@app.route('/revision/delete', methods=['GET'])
def delete_revision():
    idRevision = request.args.get('id', '')
    bdd = get_db().cursor()
    sql = "DELETE FROM revision WHERE idRevision = %s"
    bdd.execute(sql, idRevision)
    get_db().commit()
    message = u'Révision supprimé, ID: ' + idRevision
    flash(message, 'alert-danger')
    return redirect('/revision/show')
@app.route('/revision/edit', methods=['GET'])
def edit_revision():
    idRevision = request.args.get('id', '')
    bdd = get_db().cursor()
    sql = """SELECT r.*
             FROM revision r
             WHERE idRevision = %s"""
    bdd.execute(sql, (idRevision))
    revision = bdd.fetchone()
    return render_template('revision/edit_revision.html', revision=revision)
@app.route('/revision/edit', methods=['POST'])
def valid_edit_revision():
    bdd = get_db().cursor()
    idRevision = request.form.get('id-Revision', '')
    observation = request.form.get('observation', '')
    sql = """UPDATE revision
             SET observation = %s
             WHERE idRevision = %s"""
    bdd.execute(sql, [observation, idRevision])
    get_db().commit()
    message = u'Révision modifiée, ID: ' + idRevision + ', observation : ' + observation
    flash(message, 'alert-warning')
    return redirect('/revision/show')


@app.route('/typeIncident/show')
def show_typeIncident():
    bdd = get_db().cursor()
    sql = """SELECT t.*
             FROM typeIncident t
             ORDER BY t.idType"""
    bdd.execute(sql)
    typeIncident = bdd.fetchall()
    return render_template('typeIncident/show_typeIncident.html', typeIncident=typeIncident)
@app.route('/typeIncident/add', methods=['GET'])
def add_typeIncident():
    bdd = get_db().cursor()
    sql = """SELECT t.*
              FROM typeIncident t"""
    bdd.execute(sql)
    typeIncident = bdd.fetchall()
    return render_template('typeIncident/add_typeIncident.html', typeIncident=typeIncident)
@app.route('/typeIncident/add', methods=['POST'])
def valid_add_typeIncident():
    libelleType = request.form.get('libelle-Type', '')
    bdd = get_db().cursor()
    sql = """INSERT INTO typeIncident (
              libelleType)
              VALUES (%s)"""
    bdd.execute(sql,(libelleType))
    get_db().commit()
    message = u'Type d-incident ajouté, libellé : '+ libelleType
    flash(message, 'alert-success')
    return redirect('/typeIncident/show')
@app.route('/typeIncident/delete', methods=['GET'])
def delete_typeIncident():
    idType = request.args.get('id', '')
    bdd = get_db().cursor()
    sql = "DELETE FROM typeIncident WHERE idType = %s"
    bdd.execute(sql, idType)
    get_db().commit()
    message = u'Type d-incident supprimé, ID: ' + idType
    flash(message, 'alert-danger')
    return redirect('/typeIncident/show')
@app.route('/typeIncident/edit', methods=['GET'])
def edit_typeIncident():
    idType = request.args.get('id', '')
    bdd = get_db().cursor()
    sql = """SELECT t.*
             FROM typeIncident t
             WHERE idType = %s"""
    bdd.execute(sql, (idType))
    typeIncident = bdd.fetchone()
    return render_template('typeIncident/edit_typeIncident.html', typeIncident=typeIncident)
@app.route('/typeIncident/edit', methods=['POST'])
def valid_edit_typeIncident():
    bdd = get_db().cursor()
    idType = request.form.get('id-Type', '')
    libelleType = request.form.get('libelle-Type', '')
    sql = """UPDATE typeIncident
             SET libelleType = %s
             WHERE idType = %s"""
    bdd.execute(sql, [libelleType, idType])
    get_db().commit()
    message = u'Type d-incident modifié, ID: ' + idType + ', libellé type : ' + libelleType
    flash(message, 'alert-warning')
    return redirect('/typeIncident/show')


@app.route('/modele/show')
def show_modele():
    bdd = get_db().cursor()
    sql = """SELECT m.*
             FROM modele m
             ORDER BY m.idModele"""
    bdd.execute(sql)
    modele = bdd.fetchall()
    return render_template('modele/show_modele.html', modele=modele)
@app.route('/modele/add', methods=['GET'])
def add_modele():
    bdd = get_db().cursor()
    sql = """SELECT m.*
              FROM modele m"""
    bdd.execute(sql)
    modele = bdd.fetchall()
    return render_template('modele/add_modele.html', modele=modele)
@app.route('/modele/add', methods=['POST'])
def valid_add_modele():
    pression = request.form.get('pression', '')
    capacite = request.form.get('capacite', '')
    bdd = get_db().cursor()
    sql = """INSERT INTO modele (
              pression,
              capacite)
              VALUES (%s, %s)"""
    bdd.execute(sql,(pression, capacite))
    get_db().commit()
    message = u'Modèle ajouté, pression : '+ pression + ', capacité : ' + capacite
    flash(message, 'alert-success')
    return redirect('/modele/show')
@app.route('/modele/delete', methods=['GET'])
def delete_modele():
    idModele = request.args.get('id', '')
    bdd = get_db().cursor()
    sql = "DELETE FROM modele WHERE idModele = %s"
    bdd.execute(sql, idModele)
    get_db().commit()
    message = u'Modèle supprimé, ID: ' + idModele
    flash(message, 'alert-danger')
    return redirect('/modele/show')
@app.route('/modele/edit', methods=['GET'])
def edit_modele():
    idModele = request.args.get('id', '')
    bdd = get_db().cursor()
    sql = """SELECT m.*
             FROM modele m
             WHERE idModele = %s"""
    bdd.execute(sql, (idModele))
    modele = bdd.fetchone()
    return render_template('modele/edit_modele.html', modele=modele)
@app.route('/modele/edit', methods=['POST'])
def valid_edit_modele():
    bdd = get_db().cursor()
    idModele = request.form.get('id-Modele', '')
    pression = request.form.get('pression', '')
    capacite = request.form.get('capacite', '')
    sql = """UPDATE modele
             SET pression = %s,
                 capacite = %s
             WHERE idModele = %s"""
    bdd.execute(sql, [pression, capacite, idModele])
    get_db().commit()
    message = u'Modèle modifié, ID: ' + idModele + ', pression : ' + pression + ', capacité : ' + capacite
    flash(message, 'alert-warning')
    return redirect('/modele/show')


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


@app.route('/accident/show')
def show_accident():
    bdd = get_db().cursor()
    sql = """SELECT a.*, t.idType, b.idBus
             FROM accident a
             LEFT JOIN typeIncident t ON a.idType = t.idType
             LEFT JOIN bus b ON a.idBus = b.idBus
             ORDER BY a.idAccident"""
    bdd.execute(sql)
    accident = bdd.fetchall()
    return render_template('accident/show_accident.html', accident=accident)
@app.route('/accident/add', methods=['GET'])
def add_accident():
    bdd1 = get_db().cursor()
    bdd2 = get_db().cursor()
    sql1 = """SELECT t.*
              FROM typeIncident t"""
    sql2 = """SELECT b.*
              FROM bus b"""
    bdd1.execute(sql1)
    bdd2.execute(sql2)
    typeIncident = bdd1.fetchall()
    bus = bdd2.fetchall()
    return render_template('accident/add_accident.html', typeIncident=typeIncident, bus=bus)
@app.route('/accident/add', methods=['POST'])
def valid_add_accident():
    dateAccident = request.form.get('date-Accident', '')
    idType = request.form.get('id-Type', '')
    idBus = request.form.get('id-Bus', '')
    bdd = get_db().cursor()
    sql = """INSERT INTO fait (
              dateAccident,
              idType,
              idBus)
              VALUES (%s, %s, %s)"""
    bdd.execute(sql,(dateAccident, idType, idBus))
    get_db().commit()
    message = u'Accident ajouté, date de l-accident : ' + dateAccident + ', id du type d-incident: ' + idType + ', idBus : ' + idBus
    flash(message, 'alert-success')
    return redirect('/accident/show')
@app.route('/accident/delete', methods=['GET'])
def delete_accident():
    idAccident = request.args.get('id', '')
    bdd = get_db().cursor()
    sql = "DELETE FROM accident WHERE idAccident = %s"
    bdd.execute(sql, idAccident)
    get_db().commit()
    message = u'Accident supprimé, ID: ' + idAccident
    flash(message, 'alert-danger')
    return redirect('/accident/show')
@app.route('/accident/edit', methods=['GET'])
def edit_accident():
    idAccident = request.args.get('id', '')
    bdd1 = get_db().cursor()
    bdd2 = get_db().cursor()
    bdd3 = get_db().cursor()
    sql1 = """SELECT t.*
              FROM typeIncident t"""
    sql2 = """SELECT a.*
             FROM accident a
             WHERE idAccident = %s"""
    sql3 = """SELECT b.*
              FROM bus b"""
    bdd1.execute(sql1)
    bdd2.execute(sql2, (idAccident))
    bdd3.execute(sql3)
    typeIncident = bdd1.fetchall()
    accident = bdd2.fetchone()
    bus = bdd3.fetchall()
    return render_template('accident/edit_accident.html', typeIncident=typeIncident, accident=accident, bus=bus)
@app.route('/accident/edit', methods=['POST'])
def valid_edit_accident():
    bdd = get_db().cursor()
    idAccident = request.form.get('id-Accident', '')
    dateAccident = request.form.get('date-Accident', '')
    idType = request.form.get('id-Type', '')
    idBus = request.form.get('id-Bus', '')
    sql = """UPDATE accident
             SET dateAccident = %s,
                 idType = %s,
                 idBus = %s
                 WHERE idAccident = %s"""
    bdd.execute(sql, [dateAccident, idType, idBus, idAccident])
    get_db().commit()
    message = u'Accident modifié, date de l-accident : ' + dateAccident + ', id du type d-incident : '+ idType + ', Bus : ' + idBus
    flash(message, 'alert-warning')
    return redirect('/accident/show')


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
