-- Création de la base de données
CREATE DATABASE qcm_test;

-- Utilisation de la base de données
USE qcm_test;

-- Création de la table 'answer'
CREATE TABLE answer (
    idanswer INT AUTO_INCREMENT PRIMARY KEY,
    idqst INT NOT NULL,
    enonce TEXT NOT NULL,
    statut TINYINT(1) NOT NULL,
    FOREIGN KEY (idqst) REFERENCES qst(idqst)
);

-- Création de la table 'qcm'
CREATE TABLE qcm (
    idqcm INT AUTO_INCREMENT PRIMARY KEY,
    nomqcm VARCHAR(100) NOT NULL,
    categorie ENUM('THI', 'BI', 'COMPILE', 'AP', 'GL', 'RO', 'CRYPTO', 'WEB') NOT NULL,

    idprof INT NOT NULL,
    FOREIGN KEY (idprof) REFERENCES users(user_id)
);

-- Création de la table 'qcm_user'
CREATE TABLE qcm_user (
    iduser INT NOT NULL,
    idqcm INT NOT NULL,
    note FLOAT DEFAULT NULL,
    PRIMARY KEY (iduser, idqcm),
    FOREIGN KEY (iduser) REFERENCES users(user_id),
    FOREIGN KEY (idqcm) REFERENCES qcm(idqcm)
);

-- Création de la table 'qst'
CREATE TABLE qst (
    idqst INT AUTO_INCREMENT PRIMARY KEY,
    idqcm INT NOT NULL,
    enonce TEXT NOT NULL,
    FOREIGN KEY (idqcm) REFERENCES qcm(idqcm)
);

-- Création de la table 'user_rep'
CREATE TABLE user_rep (
    idrepchoisite INT NOT NULL,
    idqst INT NOT NULL,
    idqcm INT NOT NULL,
    PRIMARY KEY (idrepchoisite),
    FOREIGN KEY (idqst) REFERENCES qst(idqst),
    FOREIGN KEY (idqcm) REFERENCES qcm(idqcm)
);

-- Création de la table 'users'
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    role ENUM('prof', 'user') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    password VARCHAR(255) NOT NULL
);
