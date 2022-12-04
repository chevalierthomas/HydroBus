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
   idBus INT,
   dateAchat DATE,
   PRIMARY KEY(idBus)
);

CREATE TABLE modele(
   idModele INT,
   pression INT,
   capacite INT,
   PRIMARY KEY(idModele)
);

CREATE TABLE revision(
   IdRevision INT AUTO_INCREMENT,
   observation VARCHAR(1000),
   PRIMARY KEY(IdRevision)
);

CREATE TABLE typeIncident(
   idType INT,
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
   IdRevision INT NOT NULL,
   dateRevisionBus DATE NOT NULL,
   PRIMARY KEY(idFait),
   FOREIGN KEY(IdRevision) REFERENCES revision(IdRevision) ON DELETE CASCADE ,
   FOREIGN KEY(idBus) REFERENCES bus(idBus) ON DELETE CASCADE
);

CREATE TABLE accident(
   idAccident INT,
   dateAccident DATE NOT NULL,
   idType INT NOT NULL,
   idBus INT NOT NULL,
   PRIMARY KEY(idAccident),
   FOREIGN KEY(idType) REFERENCES typeIncident(idType),
   FOREIGN KEY(idBus) REFERENCES bus(idBus)
);

CREATE TABLE consommation(
   idConsommation INT,
   consommation INT,
   distance INT,
   annee INT NOT NULL,
   idBus INT NOT NULL,
   PRIMARY KEY(idConsommation),
   FOREIGN KEY(annee) REFERENCES anneeConsommation(annee),
   FOREIGN KEY(idBus) REFERENCES bus(idBus)
);

CREATE TABLE reservoir(
   idReservoir INT AUTO_INCREMENT,
   idModele INT NOT NULL,
   idBus INT NOT NULL,
   PRIMARY KEY(idReservoir),
   FOREIGN KEY(idModele) REFERENCES modele(idModele),
   FOREIGN KEY(idBus) REFERENCES bus(idBus)
);

CREATE TABLE recoit(
   idRecoit INT,
   dateRevisionReservoir DATE NOT NULL,
   IdRevision INT NOT NULL,
   idReservoir INT NOT NULL,
   PRIMARY KEY(idRecoit),
   FOREIGN KEY(IdRevision) REFERENCES revision(IdRevision) ON DELETE CASCADE,
   FOREIGN KEY(idReservoir) REFERENCES reservoir(idReservoir) ON DELETE CASCADE
);

INSERT INTO bus (idBus, dateAchat) VALUES
(1,'2021-02-10'),
(2,'2021-04-12'),
(3,'2021-06-14'),
(4,'2020-08-15'),
(5,'2020-10-16')
;

INSERT INTO modele (idModele,pression,capacite) VALUES
(1,56000,300),
(2,54000,320),
(3,52000,340),
(4,50000,360),
(5,48000,380)
;

INSERT INTO revision (IdRevision,observation) VALUES
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
(1,'Technique'),
(2,'Routier')
;

INSERT INTO anneeConsommation (annee) VALUES
(2020),
(2021),
(2022)
;

INSERT INTO fait (idFait, idBus,IdRevision,dateRevisionBus) VALUES
(NULL,1,1,'2022-08-01'),
(NULL,2,2,'2022-09-01'),
(NULL,3,3,'2021-08-10'),
(NULL,4,4,'2020-10-27')
;

INSERT INTO accident(idAccident, dateAccident, idType, idBus) VALUES
(1, '2022-07-27', 1, 1),
(2, '2021-12-05', 2, 2),
(3, '2022-01-19', 2, 2),
(4, '2021-11-14', 1, 1)
;

INSERT INTO consommation(idConsommation, consommation, distance, annee, idBus) VALUES
(1,84,865,2020,4),
(2,49,537,2020,5),
(3,501,18400,2021,1),
(4,431,15003,2021,2),
(5,605,19004,2021,3),
(6,900,20637,2021,4),
(7,864,19345,2021,5),
(8,999,25637,2022,1),
(9,531,18365,2022,2),
(10,405,15637,2022,3),
(11,200,9555,2022,4),
(12,684,17678,2022,5)
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

INSERT INTO recoit (idRecoit, dateRevisionReservoir, IdRevision, idReservoir) VALUES
(1,'2022-08-08',5,4),
(2,'2021-06-08',8,2)
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
*/