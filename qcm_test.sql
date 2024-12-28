CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,   
    username VARCHAR(50) NOT NULL UNIQUE,       
    name VARCHAR(100) NOT NULL,                 
    email VARCHAR(100) NOT NULL,                
    role ENUM('prof', 'user') NOT NULL,         
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    password VARCHAR(255) NOT NULL              
);

CREATE TABLE qcm ( 
    idqcm INT AUTO_INCREMENT PRIMARY KEY,
    nomqcm VARCHAR(100) NOT NULL,
    categorie ENUM('Math', 'Science', 'History') NOT NULL,
    idprof INT NOT NULL,
    FOREIGN KEY (idprof) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE TABLE qst (
    idqst INT AUTO_INCREMENT PRIMARY KEY,
    idqcm INT NOT NULL,
    enonce TEXT NOT NULL,
    FOREIGN KEY (idqcm) REFERENCES qcm(idqcm) ON DELETE CASCADE
);

CREATE TABLE answer (
    idanswer INT AUTO_INCREMENT PRIMARY KEY,
    idqst INT NOT NULL,
    enonce TEXT NOT NULL,
    statut BOOLEAN NOT NULL,
    FOREIGN KEY (idqst) REFERENCES qst(idqst) ON DELETE CASCADE
);

CREATE TABLE qcm_user (
    iduser INT NOT NULL,
    idqcm INT NOT NULL,
    note FLOAT,
    PRIMARY KEY (iduser, idqcm),
    FOREIGN KEY (iduser) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (idqcm) REFERENCES qcm(idqcm) ON DELETE CASCADE
);

CREATE TABLE user_rep (
    idrepchoisite INT NOT NULL,
    idqst INT NOT NULL,
    idqcm INT NOT NULL,
    PRIMARY KEY (idrepchoisite),
    FOREIGN KEY (idrepchoisite) REFERENCES answer(idanswer) ON DELETE CASCADE,
    FOREIGN KEY (idqst) REFERENCES qst(idqst) ON DELETE CASCADE,
    FOREIGN KEY (idqcm) REFERENCES qcm(idqcm) ON DELETE CASCADE
);
