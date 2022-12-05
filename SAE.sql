DROP TABLE IF EXISTS changement_reservoir;
DROP TABLE IF EXISTS incident;
DROP TABLE IF EXISTS kilometrage;
DROP TABLE IF EXISTS bus;
DROP TABLE IF EXISTS revision;
DROP TABLE IF EXISTS reservoir;
DROP TABLE IF EXISTS modele;
DROP TABLE IF EXISTS type_incident;

DROP TABLE IF EXISTS recoit, reservoir, consommation, accident, fait, typeIncident, revision, modele, anneeConsommation, bus;

CREATE TABLE bus(
   idBus INT AUTO_INCREMENT,
   dateAchat DATE,
   PRIMARY KEY(idBus)
);

CREATE TABLE modele(
   idModele INT AUTO_INCREMENT,
   pression INT,
   capacite INT,
   PRIMARY KEY(idModele)
);

CREATE TABLE revision(
   idRevision INT AUTO_INCREMENT,
   observation VARCHAR(1000),
   PRIMARY KEY(idRevision)
);

CREATE TABLE typeIncident(
   idType INT AUTO_INCREMENT,
   libelleType VARCHAR(50),
   PRIMARY KEY(idType)
);

CREATE TABLE anneeConsommation(
   annee INT,
   PRIMARY KEY(annee)
);

CREATE TABLE fait(
   idFait INT AUTO_INCREMENT,
   idBus INT NOT NULL,
   idRevision INT NOT NULL,
   dateRevisionBus DATE NOT NULL,
   PRIMARY KEY(idFait),
   FOREIGN KEY(idRevision) REFERENCES revision(idRevision) ON DELETE CASCADE ,
   FOREIGN KEY(idBus) REFERENCES bus(idBus) ON DELETE CASCADE
);

CREATE TABLE accident(
   idAccident INT AUTO_INCREMENT,
   dateAccident DATE NOT NULL,
   idType INT NOT NULL,
   idBus INT NOT NULL,
   PRIMARY KEY(idAccident),
   FOREIGN KEY(idType) REFERENCES typeIncident(idType) ON DELETE CASCADE ,
   FOREIGN KEY(idBus) REFERENCES bus(idBus) ON DELETE CASCADE
);

CREATE TABLE consommation(
   idConsommation INT AUTO_INCREMENT,
   nbconsommation INT,
   distance INT,
   annee INT NOT NULL,
   idBus INT NOT NULL,
   PRIMARY KEY(idConsommation),
   FOREIGN KEY(annee) REFERENCES anneeConsommation(annee) ON DELETE CASCADE ,
   FOREIGN KEY(idBus) REFERENCES bus(idBus) ON DELETE CASCADE
);

CREATE TABLE reservoir(
   idReservoir INT AUTO_INCREMENT,
   idModele INT NOT NULL,
   idBus INT NOT NULL,
   PRIMARY KEY(idReservoir),
   FOREIGN KEY(idModele) REFERENCES modele(idModele) ON DELETE CASCADE ,
   FOREIGN KEY(idBus) REFERENCES bus(idBus) ON DELETE CASCADE
);

CREATE TABLE recoit(
   idRecoit INT AUTO_INCREMENT,
   dateRevisionReservoir DATE NOT NULL,
   idRevision INT NOT NULL,
   idReservoir INT NOT NULL,
   PRIMARY KEY(idRecoit),
   FOREIGN KEY(idRevision) REFERENCES revision(idRevision) ON DELETE CASCADE,
   FOREIGN KEY(idReservoir) REFERENCES reservoir(idReservoir) ON DELETE CASCADE
);

INSERT INTO bus (idBus, dateAchat) VALUES
(NULL,'2021-02-10'),
(NULL,'2021-04-12'),
(NULL,'2021-06-14'),
(NULL,'2020-08-15'),
(NULL,'2020-10-16')
;

INSERT INTO modele (idModele,pression,capacite) VALUES
(NULL,56000,300),
(NULL,54000,320),
(NULL,52000,340),
(NULL,50000,360),
(NULL,48000,380)
;

INSERT INTO revision (idRevision,observation) VALUES
(NULL,'Rien a signaler'),
(NULL,'Pneus avants crevés à la hache'),
(NULL,'Essui glace arrondi'),
(NULL,'Pneu avant droite absent'),
(NULL,'Animal coincée dans le réservoir'),
(NULL,'Troué'),
(NULL,'Réservoir coincée'),
(NULL,'Remplie de chantilly')
;

INSERT INTO typeIncident (idType,libelleType) VALUES
(NULL,'Technique'),
(NULL,'Routier')
;

INSERT INTO anneeConsommation (annee) VALUES
(2020),
(2021),
(2022),
(2023)
;

INSERT INTO fait (idFait, idBus,idRevision,dateRevisionBus) VALUES
(NULL,1,1,'2022-08-01'),
(NULL,2,2,'2022-09-02'),
(NULL,3,3,'2021-08-10'),
(NULL,4,4,'2020-10-27'),
(NULL,5,4,'2021-01-01'),
(NULL,2,1,'2021-08-11'),
(NULL,2,3,'2020-07-07')
;

INSERT INTO accident(idAccident, dateAccident, idType, idBus) VALUES
(NULL, '2022-07-27', 1, 1),
(NULL, '2021-12-05', 2, 2),
(NULL, '2022-01-19', 2, 2),
(NULL, '2021-11-14', 1, 1)
;

INSERT INTO consommation(idConsommation, nbconsommation, distance, annee, idBus) VALUES
(NULL,84,865,2020,4),
(NULL,49,537,2020,5),
(NULL,501,18400,2021,1),
(NULL,431,15003,2021,2),
(NULL,605,19004,2021,3),
(NULL,900,20637,2021,4),
(NULL,864,19345,2021,5),
(NULL,999,25637,2022,1),
(NULL,531,18365,2022,2),
(NULL,405,15637,2022,3),
(NULL,200,9555,2022,4),
(NULL,684,17678,2022,5)
;

INSERT INTO reservoir (idReservoir,idModele,idBus) VALUES
(NULL,5,1),
(NULL,1,2),
(NULL,3,3),
(NULL,2,4),
(NULL,1,5),
(NULL,4,1),
(NULL,1,5),
(NULL,2,3)
;

INSERT INTO recoit (idRecoit, dateRevisionReservoir, idRevision, idReservoir) VALUES
(NULL,'2022-08-08',5,4),
(NULL,'2021-06-08',8,2)
;

/* SELECT * FROM bus;
SELECT * FROM modele;
SELECT * FROM revision;
SELECT * FROM typeIncident;
SELECT * FROM anneeConsommation;
SELECT * FROM fait;
SELECT * FROM accident;
SELECT * FROM consommation;
SELECT * FROM reservoir;
SELECT * FROM recoit;

SELECT * FROM fait
WHERE dateRevisionBus IN (SELECT max(dateRevisionBus) FROM fait);
*/
