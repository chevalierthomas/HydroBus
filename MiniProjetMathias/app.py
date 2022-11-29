#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Flask, request, render_template, redirect, url_for, abort, flash

app = Flask(__name__)
app.secret_key = 'une cle(token) : grain de sel(any random string)'



departements=[

    {'id':1, 'nomDepartement':'Bouche du Rhône'},
    {'id':2, 'nomDepartement':'Gard'},
    {'id':3, 'nomDepartement':'Vaucluse'},
]

monuments = [
    {'id':1,'nomMonument':'Château d If', 'description':'description Château d If', 'dateCreation':'1529-01-01', 'noteMichelin':4, 'departement_id':1, 'prix':10.5},
    {'id':2,'nomMonument':'Basilique Notre-Dame de la Garde', 'description':'description Basilic Notre-Dame de la Garde', 'dateCreation':'1700-08-09', 'noteMichelin':3, 'departement_id':1, 'prix':0},
    {'id':3,'nomMonument':'Pont du Gard', 'description':'description Pont du Gard', 'dateCreation':'0500-01-01', 'noteMichelin':5, 'departement_id':2, 'prix':15},
    {'id':4,'nomMonument':'La Maison Carrée', 'description':'description La Masion Carrée', 'dateCreation':'0500-01-01', 'noteMichelin':4, 'departement_id':2, 'prix':10.5},
    {'id':5,'nomMonument':'Palais des Papes', 'description':'description Palais des Papes', 'dateCreation':'1500-09-09', 'noteMichelin':5, 'departement_id':1, 'prix':6},
    {'id':6,'nomMonument':'Musée du Petit Palais', 'description':'description Musée du Petit Palais', 'dateCreation':'1900-08-09', 'noteMichelin':4, 'departement_id':1, 'prix':5}
]

@app.route('/')
def show_accueil():
    return render_template('layout.html')

@app.route('/toggle/toggle')
def show_toggle():
    return render_template('toggle/toggle.html', departements=departements, monuments=monuments)

@app.route('/departements/show')
def show_departements():
    return render_template('departements/show_departements.html', departements=departements)

@app.route('/departements/add', methods=['GET'])
def add_departements():
    return render_template('departements/add_departements.html')

@app.route('/departements/add', methods=['POST'])
def valid_add_departements():
    nomDepartement = request.form.get('libelle', '')
    print(u'type ajouté , libellé : ', nomDepartement)
    message = u'type ajouté , libellé : ' + nomDepartement
    flash(message, 'alert-success')
    return redirect('/departements/show')

@app.route('/departements/delete', methods=['GET'])
def delete_departements():
    id = request.args.get('id', '')
    print("un département supprimé, id : ", id)
    message = u'un département supprimé, id : ' + id
    flash(message, 'alert-warning')
    return redirect('/departements/show')

@app.route('/departements/edit', methods=['GET'])
def edit_departements():
    id = request.args.get('id', '')
    id = int(id)
    departement = departements[id-1]
    return render_template('departements/edit_departements.html', departements=departement)

@app.route('/departements/edit', methods=['POST'])
def valid_edit_departements():
    nomDepartement = request.form['nomDepartement']
    id = request.form.get('id', '')
    print(u'département modifié, id : ',id, " libelle : ", nomDepartement)
    message=u'département modifié, id : ' + id + " libelle : " + nomDepartement
    flash(message, 'alert-success')
    return redirect('/departements/show')

@app.route('/monuments/show')
def show_monuments():
    return render_template('monuments/show_monuments.html', monuments=monuments)

@app.route('/monuments/add', methods=['GET'])
def add_monuments():
    return render_template('monuments/add_monuments.html', departements=departements)

@app.route('/monuments/add', methods=['POST'])
def valid_add_monuments():
    nomMonument = request.form.get('nom', '')
    description = request.form.get('description', '')
    dateCreation = request.form.get('dateCreation', '')
    noteMichelin = request.form.get('noteMichelin', '')
    departement_id = request.form.get('departement_id', '')
    prix = request.form.get('prix', '')
    print(u'monument ajouté , nom : ', nomMonument, ' - description : ', description, ' - date de creation : ', dateCreation, ' - note Michelin : ', noteMichelin, ' - id du departement : ', departement_id, ' - prix : ', prix)
    message = u'monument ajouté , nom : ' + nomMonument + ' - description :' + description + ' - date de creation : ' + dateCreation + ' - note Michelin : ' + noteMichelin + ' - id du departement : ' + departement_id + ' - prix : ' + prix
    flash(message, 'alert-success')
    return redirect('/monuments/show')

@app.route('/monuments/delete', methods=['GET'])
def delete_monuments():
    id = request.args.get('id', '')
    message='un monument supprimé, id : ' + id
    flash(message, 'alert-warning')
    return redirect('/monuments/show')

@app.route('/monuments/edit', methods=['GET'])
def edit_monuments():
    id = request.args.get('id', '')
    id = int(id)
    monument = monuments[id-1]
    return render_template('monuments/edit_monuments.html', departements=departements, monuments=monument)

@app.route('/monuments/edit', methods=['POST'])
def valid_edit_monuments():
    id = request.form.get('id', '')
    nomMonument = request.form.get('nomMonument', '')
    prix = request.form.get('prix', '')
    noteMichelin = request.form.get('noteMichelin', '')
    dateCreation = request.form.get('dateCreation', '')
    description = request.form.get('description', '')

    departement_id = request.form.get('departement_id', '')

    message = u'id : ' + id + ' - nom : ' + nomMonument + ' - prix : ' + prix + ' - noteMichelin : ' + noteMichelin + ' - dateCreation : ' + dateCreation + ' - description : ' + description + ' - departement_id : ' + departement_id
    flash(message, 'alert-success')
    return redirect('/monuments/show')

if __name__ == '__main__':
    app.run()
