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
#departements=[
#    {'id':1, 'nomDepartement':'Bouche du Rhône'},
#    {'id':2, 'nomDepartement':'Gard'},
#    {'id':3, 'nomDepartement':'Vaucluse'},
#]

#monuments = [
#    {'id':1,'nomMonument':'Château d If', 'description':'description Château d If', 'dateCreation':'1529-01-01', 'noteMichelin':4, 'departement_id':1, 'prix':10.5},
#    {'id':2,'nomMonument':'Basilique Notre-Dame de la Garde', 'description':'description Basilic Notre-Dame de la Garde', 'dateCreation':'1700-08-09', 'noteMichelin':3, 'departement_id':1, 'prix':0},
#    {'id':3,'nomMonument':'Pont du Gard', 'description':'description Pont du Gard', 'dateCreation':'0500-01-01', 'noteMichelin':5, 'departement_id':2, 'prix':15},
#    {'id':4,'nomMonument':'La Maison Carrée', 'description':'description La Masion Carrée', 'dateCreation':'0500-01-01', 'noteMichelin':4, 'departement_id':2, 'prix':10.5},
#    {'id':5,'nomMonument':'Palais des Papes', 'description':'description Palais des Papes', 'dateCreation':'1500-09-09', 'noteMichelin':5, 'departement_id':1, 'prix':6},
#    {'id':6,'nomMonument':'Musée du Petit Palais', 'description':'description Musée du Petit Palais', 'dateCreation':'1900-08-09', 'noteMichelin':4, 'departement_id':1, 'prix':5}
#]

@app.route('/')
def show_accueil():
    return render_template('layout.html')

@app.route('/accident/show')
def show_accident():
    return render_template('accident/show_accident.html')
@app.route('/accident/add', methods=['GET'])
def add_accident():
    return render_template('accident/add_accident.html')
@app.route('/accident/add', methods=['POST'])
def valid_add_accident():
    return redirect('/accident/show')
@app.route('/accident/delete', methods=['GET'])
def delete_accident():
    return redirect('/accident/show')
@app.route('/accident/delete', methods=['POST'])
def valid_delete_accident():
    return redirect('/accident/show')
@app.route('/accident/edit', methods=['GET'])
def edit_accident():
    return render_template('accident/edit_accident.html')
@app.route('/accident/edit', methods=['POST'])
def valid_edit_accident():
    return redirect('/accident/show')

@app.route('/anneeConsommation/show')
def show_anneeConsommation():
    return render_template('anneeConsommation/show_anneeConsommation.html')
@app.route('/anneeConsommation/add', methods=['GET'])
def add_anneeConsommation():
    return render_template('anneeConsommation/add_anneeConsommation.html')
@app.route('/anneeConsommation/add', methods=['POST'])
def valid_add_anneeConsommation():
    return redirect('/anneeConsommation/show')
@app.route('/anneeConsommation/delete', methods=['GET'])
def delete_anneeConsommation():
    return redirect('/anneeConsommation/show')
@app.route('/anneeConsommation/delete', methods=['POST'])
def valid_delete_anneeConsommation():
    return redirect('/anneeConsommation/show')
@app.route('/anneeConsommation/edit', methods=['GET'])
def edit_anneeConsommation():
    return render_template('anneeConsommation/edit_anneeConsommation.html')
@app.route('/anneeConsommation/edit', methods=['POST'])
def valid_edit_anneeConsommation():
    return redirect('/anneeConsommation/show')

@app.route('/bus/show')
def show_bus():
    return render_template('bus/show_bus.html')
@app.route('/bus/add', methods=['GET'])
def add_bus():
    return render_template('bus/add_bus.html')
@app.route('/bus/add', methods=['POST'])
def valid_add_bus():
    return redirect('/bus/show')
@app.route('/bus/delete', methods=['GET'])
def delete_bus():
    return redirect('/bus/show')
@app.route('/bus/delete', methods=['POST'])
def valid_delete_bus():
    return redirect('/bus/show')
@app.route('/bus/edit', methods=['GET'])
def edit_bus():
    return render_template('bus/edit_bus.html')
@app.route('/bus/edit', methods=['POST'])
def valid_edit_bus():
    return redirect('/bus/show')

@app.route('/consommation/show')
def show_consommation():
    return render_template('consommation/show_consommation.html')
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

@app.route('/fait/show')
def show_fait():
    return render_template('fait/show_fait.html')
@app.route('/fait/add', methods=['GET'])
def add_fait():
    return render_template('fait/add_fait.html')
@app.route('/fait/add', methods=['POST'])
def valid_add_fait():
    return redirect('/fait/show')
@app.route('/fait/delete', methods=['GET'])
def delete_fait():
    return redirect('/fait/show')
@app.route('/fait/delete', methods=['POST'])
def valid_delete_fait():
    return redirect('/fait/show')
@app.route('/fait/edit', methods=['GET'])
def edit_fait():
    return render_template('fait/edit_fait.html')
@app.route('/fait/edit', methods=['POST'])
def valid_edit_fait():
    return redirect('/fait/show')

@app.route('/modele/show')
def show_modele():
    return render_template('modele/show_modele.html')
@app.route('/modele/add', methods=['GET'])
def add_modele():
    return render_template('modele/add_modele.html')
@app.route('/modele/add', methods=['POST'])
def valid_add_modele():
    return redirect('/modele/show')
@app.route('/modele/delete', methods=['GET'])
def delete_modele():
    return redirect('/modele/show')
@app.route('/modele/delete', methods=['POST'])
def valid_delete_modele():
    return redirect('/modele/show')
@app.route('/modele/edit', methods=['GET'])
def edit_modele():
    return render_template('modele/edit_modele.html')
@app.route('/modele/edit', methods=['POST'])
def valid_edit_modele():
    return redirect('/modele/show')

@app.route('/recoit/show')
def show_recoit():
    return render_template('recoit/show_recoit.html')
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

@app.route('/reservoir/show')
def show_reservoir():
    return render_template('reservoir/show_reservoir.html')
@app.route('/reservoir/add', methods=['GET'])
def add_reservoir():
    return render_template('reservoir/add_reservoir.html')
@app.route('/reservoir/add', methods=['POST'])
def valid_add_reservoir():
    return redirect('/reservoir/show')
@app.route('/reservoir/delete', methods=['GET'])
def delete_reservoir():
    return redirect('/reservoir/show')
@app.route('/reservoir/delete', methods=['POST'])
def valid_delete_reservoir():
    return redirect('/reservoir/show')
@app.route('/reservoir/edit', methods=['GET'])
def edit_reservoir():
    return render_template('reservoir/edit_reservoir.html')
@app.route('/reservoir/edit', methods=['POST'])
def valid_edit_reservoir():
    return redirect('/reservoir/show')

@app.route('/revision/show')
def show_revision():
    return render_template('revision/show_revision.html')
@app.route('/revision/add', methods=['GET'])
def add_revision():
    return render_template('revision/add_revision.html')
@app.route('/revision/add', methods=['POST'])
def valid_add_revision():
    return redirect('/revision/show')
@app.route('/revision/delete', methods=['GET'])
def delete_revision():
    return redirect('/revision/show')
@app.route('/revision/delete', methods=['POST'])
def valid_delete_revision():
    return redirect('/revision/show')
@app.route('/revision/edit', methods=['GET'])
def edit_revision():
    return render_template('revision/edit_revision.html')
@app.route('/revision/edit', methods=['POST'])
def valid_edit_revision():
    return redirect('/revision/show')

@app.route('/typeIncident/show')
def show_typeIncident():
    return render_template('typeIncident/show_typeIncident.html')
@app.route('/typeIncident/add', methods=['GET'])
def add_typeIncident():
    return render_template('typeIncident/add_typeIncident.html')
@app.route('/typeIncident/add', methods=['POST'])
def valid_add_typeIncident():
    return redirect('/typeIncident/show')
@app.route('/typeIncident/delete', methods=['GET'])
def delete_typeIncident():
    return redirect('/typeIncident/show')
@app.route('/typeIncident/delete', methods=['POST'])
def valid_delete_typeIncident():
    return redirect('/typeIncident/show')
@app.route('/typeIncident/edit', methods=['GET'])
def edit_typeIncident():
    return render_template('typeIncident/edit_typeIncident.html')
@app.route('/typeIncident/edit', methods=['POST'])
def valid_edit_typeIncident():
    return redirect('/typeIncident/show')
if __name__ == '__main__':
    app.run()
