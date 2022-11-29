DROP TABLE IF EXISTS  bus, modele, revision, typeIncident, anneeConsommation, reservoir, consomme, subit, fait, recoit;

CREATE TABLE bus(
   idBus INT AUTO_INCREMENT,
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
   idModele INT AUTO_INCREMENT,
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
   IdRevision INT AUTO_INCREMENT,
   observation VARCHAR(1000),
   PRIMARY KEY(IdRevision)
);

INSERT INTO revision (IdRevision,observation) VALUES
(1,'Rien a signaler'),
(2,'Pneus avants crevés à la hache'),
(3,'Essui glace arrondi'),
(4,'Pneu avant droite absent')
;

CREATE TABLE typeIncident(
   idType INT AUTO_INCREMENT,
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

CREATE TABLE reservoir(
   idReservoir INT AUTO_INCREMENT,
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

CREATE TABLE consomme(
   idBus INT,
   annee INT,
   consommation INT,
   distance INT,
   PRIMARY KEY(idBus, annee),
   FOREIGN KEY(idBus) REFERENCES bus(idBus),
   FOREIGN KEY(annee) REFERENCES anneeConsommation(annee)
);

INSERT INTO consomme (idBus,annee,consommation,distance) VALUES
(1,2020,531,18365),
(2,2021,405,15637)
;

CREATE TABLE subit(
   idBus INT,
   idType INT,
   PRIMARY KEY(idBus, idType),
   FOREIGN KEY(idBus) REFERENCES bus(idBus),
   FOREIGN KEY(idType) REFERENCES typeIncident(idType)
);

INSERT INTO subit (idBus,idType) VALUES
(1,1),
(2,2),
(3,2),
(5,1)
;

CREATE TABLE fait(
   idBus INT,
   IdRevision INT,
   dateRevisionBus DATE,
   PRIMARY KEY(idBus, IdRevision),
   FOREIGN KEY(idBus) REFERENCES bus(idBus),
   FOREIGN KEY(IdRevision) REFERENCES revision(IdRevision)
);

INSERT INTO fait (idBus,IdRevision,dateRevisionBus) VALUES
(1,1,'2022-08-01'),
(2,2,'2022-09-01'),
(3,3,'2021-08-10'),
(3,4,'2020-10-27')
;

CREATE TABLE recoit(
   idReservoir INT,
   IdRevision INT,
   dateRevisionReservoir DATE,
   PRIMARY KEY(idReservoir, IdRevision),
   FOREIGN KEY(idReservoir) REFERENCES reservoir(idReservoir),
   FOREIGN KEY(IdRevision) REFERENCES revision(IdRevision)
);

INSERT INTO recoit (idReservoir,IdRevision,dateRevisionReservoir) VALUES
(1,2,'2022-08-08'),
(2,4,'2021-06-08')
;


#Tous les bus achetés en 2020 trié par ordre chronologique
SELECT idbus, dateAchat
FROM bus
WHERE (year(dateAchat)) = 2020
ORDER BY dateAchat
;

#Tous les id des bus ayant subit un incident routier
SELECT libelleType,b.idBus
FROM typeIncident
JOIN subit s on typeIncident.idType = s.idType
JOIN bus b on s.idBus = b.idBus
WHERE(typeIncident.idType) = 2
;

#Tous les id de modèle de réservoir ayant appartenu a un bus ayant fait une revision
SELECT modele.idmodele, pression, capacite
FROM modele
JOIN reservoir r on modele.idModele = r.idModele
JOIN bus b on r.idBus = b.idBus
JOIN fait f on b.idBus = f.idBus
JOIN revision r2 on f.IdRevision = r2.IdRevision
WHERE(f.IdRevision)
ORDER BY idModele
;