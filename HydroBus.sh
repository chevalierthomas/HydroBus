#!/bin/bash

wine /opt/looping-mcd/Looping.exe mcd.loo
mysql --user=login  --password=motDePasse --host=serveurmysql --database=BDD_login < sql_projet.sql
python3 app.py
