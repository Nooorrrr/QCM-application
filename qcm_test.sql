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

-- Inserting fake data into the 'qcm' table
INSERT INTO qcm (nomqcm, categorie, idprof) VALUES 
('QCM Théorie de l\'information', 'THI', 1),
('QCM Business Intelligence', 'BI', 1),
('QCM Compilation', 'COMPILE', 1),
('QCM Python', 'AP', 1),
('QCM Génie Logiciel', 'GL', 1),
('QCM Recherche Opérationnelle', 'RO', 1),
('QCM Cryptographie', 'CRYPTO', 1),
('QCM Développement Web', 'WEB', 1);

-- Inserting fake data into the 'qst' table
INSERT INTO qst (idqcm, enonce) VALUES 
(1, 'Qu\'est-ce que l\'entropie en théorie de l\'information ?'),
(1, 'Quelle est la formule de Shannon pour l\'entropie ?'),
(2, 'Qu\'est-ce que l\'ETL en Business Intelligence ?'),
(2, 'Quelle est la différence entre OLAP et OLTP ?'),
(3, 'Qu\'est-ce qu\'un compilateur ?'),
(3, 'Quelle est la différence entre un compilateur et un interpréteur ?'),
(4, 'Qu\'est-ce qu\'une liste en Python ?'),
(4, 'Quelle est la différence entre une liste et un tuple en Python ?'),
(5, 'Qu\'est-ce que le modèle MVC en génie logiciel ?'),
(5, 'Quelle est la différence entre une classe et un objet ?'),
(6, 'Qu\'est-ce que la programmation linéaire en recherche opérationnelle ?'),
(6, 'Quelle est la méthode du simplexe ?'),
(7, 'Qu\'est-ce que le chiffrement symétrique ?'),
(7, 'Quelle est la différence entre chiffrement symétrique et asymétrique ?'),
(8, 'Qu\'est-ce qu\'un framework de développement web ?'),
(8, 'Quelle est la différence entre HTML et CSS ?');

-- Inserting fake data into the 'answer' table
INSERT INTO answer (idqst, enonce, statut) VALUES 
(1, 'Mesure de l\'incertitude', 1),
(1, 'Mesure de la redondance', 0),
(2, 'H(X) = -Σ p(x) log p(x)', 1),
(2, 'H(X) = Σ p(x) log p(x)', 0),
(3, 'Processus d\'extraction, transformation et chargement des données', 1),
(3, 'Processus de modification des données', 0),
(4, 'OLAP est pour l\'analyse, OLTP est pour les transactions', 1),
(4, 'OLAP est pour les transactions, OLTP est pour l\'analyse', 0),
(5, 'Programme qui traduit le code source en code machine', 1),
(5, 'Programme qui exécute le code source directement', 0),
(6, 'Le compilateur traduit, l\'interpréteur exécute', 1),
(6, 'Le compilateur exécute, l\'interpréteur traduit', 0),
(7, 'Structure de données mutable', 1),
(7, 'Structure de données immuable', 0),
(8, 'Liste est mutable, tuple est immuable', 1),
(8, 'Liste est immuable, tuple est mutable', 0),
(9, 'Modèle de conception logicielle', 1),
(9, 'Langage de programmation', 0),
(10, 'Classe est un modèle, objet est une instance', 1),
(10, 'Classe est une instance, objet est un modèle', 0),
(11, 'Méthode pour optimiser un objectif linéaire', 1),
(11, 'Méthode pour résoudre des équations différentielles', 0),
(12, 'Algorithme pour résoudre des problèmes de programmation linéaire', 1),
(12, 'Algorithme pour trier des données', 0),
(13, 'Utilise une seule clé pour chiffrer et déchiffrer', 1),
(13, 'Utilise deux clés différentes', 0),
(14, 'Symétrique utilise une clé, asymétrique utilise deux clés', 1),
(14, 'Symétrique utilise deux clés, asymétrique utilise une clé', 0),
(15, 'Environnement de développement pour applications web', 1),
(15, 'Langage de programmation', 0),
(16, 'HTML structure, CSS style', 1),
(16, 'HTML style, CSS structure', 0);
