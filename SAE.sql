DROP TABLE IF EXISTS bus, modele, revision, typeIncident, anneeConsommation, fait, accident, consommation, reservoir, recoit;

CREATE TABLE bus(
   idBus INT,
   dateAchat DATE,
   PRIMARY KEY(idBus)
);

INSERT INTO bus (idBus, dateAchat) VALUES
(1,'2021-02-10'),
(2,'2021-04-12'),
(3,'2021-06-14'),
(4,'2020-08-15'),
(5,'2020-10-16')
;

CREATE TABLE modele(
   idModele INT,
   pression INT,
   capacite INT,
   PRIMARY KEY(idModele)
);

INSERT INTO modele (idModele,pression,capacite) VALUES
(1,56000,300),
(2,54000,320),
(3,52000,340),
(4,50000,360),
(5,48000,380)
;

CREATE TABLE revision(
   IdRevision INT,
   observation VARCHAR(1000),
   PRIMARY KEY(IdRevision)
);

INSERT INTO revision (IdRevision,observation) VALUES
(1,'Rien a signaler'),
(2,'Pneus avants crevés à la hache'),
(3,'Essui glace arrondi'),
(4,'Pneu avant droite absent'),
(5,'Animal coincée dans le réservoir'),
(6,'Troué'),
(7,'Réservoir coincée'),
(8,'Remplie de chantilly')
;

CREATE TABLE typeIncident(
   idType INT,
   libelleType VARCHAR(50),
   PRIMARY KEY(idType)
);

INSERT INTO typeIncident (idType,libelleType) VALUES
(1,'Technique'),
(2,'Routier')
;

CREATE TABLE anneeConsommation(
   annee INT,
   PRIMARY KEY(annee)
);

INSERT INTO anneeConsommation (annee) VALUES
(2020),
(2021),
(2022)
;

CREATE TABLE fait(
   idFait INT,
   idBus INT NOT NULL,
   IdRevision INT NOT NULL,
   dateRevisionBus DATE NOT NULL,
   PRIMARY KEY(idFait),
   FOREIGN KEY(IdRevision) REFERENCES revision(IdRevision),
   FOREIGN KEY(idBus) REFERENCES bus(idBus)
);

INSERT INTO fait (idFait, idBus,IdRevision,dateRevisionBus) VALUES
(1,1,1,'2022-08-01'),
(2,2,2,'2022-09-01'),
(3,3,3,'2021-08-10'),
(4,4,4,'2020-10-27')
;

CREATE TABLE accident(
   idAccident INT,
   dateAccident DATE NOT NULL,
   idType INT NOT NULL,
   idBus INT NOT NULL,
   PRIMARY KEY(idAccident),
   FOREIGN KEY(idType) REFERENCES typeIncident(idType),
   FOREIGN KEY(idBus) REFERENCES bus(idBus)
);

INSERT INTO accident(idAccident, dateAccident, idType, idBus) VALUES
(1, '2022-07-27', 1, 1),
(2, '2021-12-05', 2, 2),
(3, '2022-01-19', 2, 2),
(4, '2021-11-14', 1, 1)
;

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

CREATE TABLE reservoir(
   idReservoir INT,
   idModele INT NOT NULL,
   idBus INT NOT NULL,
   PRIMARY KEY(idReservoir),
   FOREIGN KEY(idModele) REFERENCES modele(idModele),
   FOREIGN KEY(idBus) REFERENCES bus(idBus)
);

INSERT INTO reservoir (idReservoir,idModele,idBus) VALUES
(1,5,1),
(2,1,2),
(3,3,3),
(4,2,4),
(5,1,5),
(6,4,1),
(7,1,5),
(8,2,3)
;

CREATE TABLE recoit(
   idRecoit INT,
   dateRevisionReservoir DATE NOT NULL,
   IdRevision INT NOT NULL,
   idReservoir INT NOT NULL,
   PRIMARY KEY(idRecoit),
   FOREIGN KEY(IdRevision) REFERENCES revision(IdRevision),
   FOREIGN KEY(idReservoir) REFERENCES reservoir(idReservoir)
);

INSERT INTO recoit (idRecoit, dateRevisionReservoir, IdRevision, idReservoir) VALUES
(1,'2022-08-08',5,4),
(2,'2021-06-08',8,2)
;