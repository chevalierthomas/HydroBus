CREATE TABLE bus(
   idBus INT,
   dateAchat DATE,
   PRIMARY KEY(idBus)
);

CREATE TABLE modele(
   idModele INT,
   pression INT,
   capacité INT,
   PRIMARY KEY(idModele)
);

CREATE TABLE revision(
   IdRevision INT,
   observation VARCHAR(1000),
   PRIMARY KEY(IdRevision)
);

CREATE TABLE typeIncident(
   idType INT,
   libelleType VARCHAR(50),
   PRIMARY KEY(idType)
);

CREATE TABLE anneeConsommation(
   annee DATE,
   PRIMARY KEY(annee)
);

CREATE TABLE fait(
   idFait INT,
   dateRevisionBus DATE NOT NULL,
   IdRevision INT NOT NULL,
   idBus INT NOT NULL,
   PRIMARY KEY(idFait),
   FOREIGN KEY(IdRevision) REFERENCES revision(IdRevision),
   FOREIGN KEY(idBus) REFERENCES bus(idBus)
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
   annee DATE NOT NULL,
   idBus INT NOT NULL,
   PRIMARY KEY(idConsommation),
   FOREIGN KEY(annee) REFERENCES anneeConsommation(annee),
   FOREIGN KEY(idBus) REFERENCES bus(idBus)
);

CREATE TABLE reservoir(
   idReservoir INT,
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
   FOREIGN KEY(IdRevision) REFERENCES revision(IdRevision),
   FOREIGN KEY(idReservoir) REFERENCES reservoir(idReservoir)
);