
SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `qcm_test`
--

-- --------------------------------------------------------


CREATE TABLE `answer` (
  `idanswer` int NOT NULL,
  `idqst` int NOT NULL,
  `enonce` text NOT NULL,
  `statut` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Gegevens worden geëxporteerd voor tabel `answer`
--

INSERT INTO `answer` (`idanswer`, `idqst`, `enonce`, `statut`) VALUES
(1, 17, 'Mesure de l\'incertitude', 1),
(2, 17, 'Mesure de la redondance', 0),
(3, 18, 'H(X) = -Σ p(x) log p(x)', 1),
(4, 18, 'H(X) = Σ p(x) log p(x)', 0),
(5, 19, 'Processus d\'extraction, transformation et chargement des données', 1),
(6, 19, 'Processus de modification des données', 0),
(7, 20, 'OLAP est pour l\'analyse, OLTP est pour les transactions', 1),
(8, 20, 'OLAP est pour les transactions, OLTP est pour l\'analyse', 0),
(9, 21, 'Programme qui traduit le code source en code machine', 1),
(10, 21, 'Programme qui exécute le code source directement', 0),
(11, 22, 'Le compilateur traduit, l\'interpréteur exécute', 1),
(12, 22, 'Le compilateur exécute, l\'interpréteur traduit', 0),
(13, 23, 'Structure de données mutable', 1),
(14, 23, 'Structure de données immuable', 0),
(15, 24, 'Liste est mutable, tuple est immuable', 1),
(16, 24, 'Liste est immuable, tuple est mutable', 0),
(17, 25, 'Modèle de conception logicielle', 1),
(18, 25, 'Langage de programmation', 0),
(19, 26, 'Classe est un modèle, objet est une instance', 1),
(20, 26, 'Classe est une instance, objet est un modèle', 0),
(21, 27, 'Méthode pour optimiser un objectif linéaire', 1),
(22, 27, 'Méthode pour résoudre des équations différentielles', 0),
(23, 28, 'Algorithme pour résoudre des problèmes de programmation linéaire', 1),
(24, 28, 'Algorithme pour trier des données', 0),
(25, 29, 'Utilise une seule clé pour chiffrer et déchiffrer', 1),
(26, 29, 'Utilise deux clés différentes', 0),
(27, 30, 'Symétrique utilise une clé, asymétrique utilise deux clés', 1),
(28, 30, 'Symétrique utilise deux clés, asymétrique utilise une clé', 0),
(29, 31, 'Environnement de développement pour applications web', 1),
(30, 31, 'Langage de programmation', 0),
(31, 32, 'HTML structure, CSS style', 1),
(32, 32, 'HTML style, CSS structure', 0),
(33, 33, 'a title tag', 1),
(34, 33, 'wrong answer', 0),
(35, 34, '1a', 1),
(36, 34, 'test11', 0),
(37, 34, 'te_te', 0);

-- --------------------------------------------------------

--
-- Tabelstructuur voor tabel `qcm`
--

CREATE TABLE `qcm` (
  `idqcm` int NOT NULL,
  `nomqcm` varchar(100) NOT NULL,
  `categorie` enum('THI','BI','COMPILE','AP','GL','RO','CRYPTO','WEB') NOT NULL,
  `idprof` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Gegevens worden geëxporteerd voor tabel `qcm`
--

INSERT INTO `qcm` (`idqcm`, `nomqcm`, `categorie`, `idprof`) VALUES
(9, 'QCM Théorie de l\'information', 'THI', 1),
(10, 'QCM Business Intelligence', 'BI', 1),
(11, 'QCM Compilation', 'COMPILE', 1),
(12, 'QCM Python', 'AP', 1),
(13, 'QCM Génie Logiciel', 'GL', 1),
(14, 'QCM Recherche Opérationnelle', 'RO', 1),
(15, 'QCM Cryptographie', 'CRYPTO', 1),
(16, 'QCM Développement Web', 'WEB', 1),
(25, 'web dev', 'WEB', 1),
(26, 'beginner python qcm', 'AP', 1);

-- --------------------------------------------------------

--
-- Tabelstructuur voor tabel `qcm_user`
--

CREATE TABLE `qcm_user` (
  `iduser` int NOT NULL,
  `idqcm` int NOT NULL,
  `note` float DEFAULT NULL,
  `timestamp` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Gegevens worden geëxporteerd voor tabel `qcm_user`
--

INSERT INTO `qcm_user` (`iduser`, `idqcm`, `note`, `timestamp`) VALUES
(2, 9, 50, '2025-01-23 09:56:12'),
(2, 12, 50, '2025-01-23 10:02:06'),
(2, 14, 50, '2025-01-23 10:10:33'),
(2, 15, 50, '2025-01-23 10:27:16'),
(2, 16, 50, '2025-01-23 10:25:56'),
(2, 26, 100, '2025-01-23 10:29:36');

-- --------------------------------------------------------

--
-- Tabelstructuur voor tabel `qst`
--

CREATE TABLE `qst` (
  `idqst` int NOT NULL,
  `idqcm` int NOT NULL,
  `enonce` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Gegevens worden geëxporteerd voor tabel `qst`
--

INSERT INTO `qst` (`idqst`, `idqcm`, `enonce`) VALUES
(17, 9, 'Qu\'est-ce que l\'entropie en théorie de l\'information ?'),
(18, 9, 'Quelle est la formule de Shannon pour l\'entropie ?'),
(19, 10, 'Qu\'est-ce que l\'ETL en Business Intelligence ?'),
(20, 10, 'Quelle est la différence entre OLAP et OLTP ?'),
(21, 11, 'Qu\'est-ce qu\'un compilateur ?'),
(22, 11, 'Quelle est la différence entre un compilateur et un interpréteur ?'),
(23, 12, 'Qu\'est-ce qu\'une liste en Python ?'),
(24, 12, 'Quelle est la différence entre une liste et un tuple en Python ?'),
(25, 13, 'Qu\'est-ce que le modèle MVC en génie logiciel ?'),
(26, 13, 'Quelle est la différence entre une classe et un objet ?'),
(27, 14, 'Qu\'est-ce que la programmation linéaire en recherche opérationnelle ?'),
(28, 14, 'Quelle est la méthode du simplexe ?'),
(29, 15, 'Qu\'est-ce que le chiffrement symétrique ?'),
(30, 15, 'Quelle est la différence entre chiffrement symétrique et asymétrique ?'),
(31, 16, 'Qu\'est-ce qu\'un framework de développement web ?'),
(32, 16, 'Quelle est la différence entre HTML et CSS ?'),
(33, 25, 'what is the H1 do ?'),
(34, 26, 'which variable is declared wrong');

-- --------------------------------------------------------

--
-- Tabelstructuur voor tabel `users`
--

CREATE TABLE `users` (
  `user_id` int NOT NULL,
  `username` varchar(50) NOT NULL,
  `name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `role` enum('prof','user') NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `password` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Gegevens worden geëxporteerd voor tabel `users`
--

INSERT INTO `users` (`user_id`, `username`, `name`, `email`, `role`, `created_at`, `password`) VALUES
(1, 'admin', 'Admin User', 'admin@example.com', 'prof', '2025-01-23 09:08:28', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8'),
(2, 'noor', 'noor', 'noor@gmail.com', 'user', '2025-01-23 09:15:33', '92a70799e19d8734fecfb8e59aa930e9f386f7645059a1f2f04eb8483c9b5f1d'),
(3, 'test', 'testuser', 'test@gmail.com', 'user', '2025-01-23 10:03:10', '822e54d37dd37d83776ed8aac05e4578e8b201d8f3fa366bdc60b75228bc835f'),
(4, 'user', 'usertest', 'useruser@gmail.com', 'user', '2025-01-23 10:11:18', '04f8996da763b7a969b1028ee3007569eaf3a635486ddab211d512c85b9df8fb');

-- --------------------------------------------------------

--
-- Tabelstructuur voor tabel `user_rep`
--

CREATE TABLE `user_rep` (
  `idrepchoisite` int NOT NULL,
  `idqst` int NOT NULL,
  `idqcm` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Indexen voor geëxporteerde tabellen
--

--
-- Indexen voor tabel `answer`
--
ALTER TABLE `answer`
  ADD PRIMARY KEY (`idanswer`),
  ADD KEY `idqst` (`idqst`);

--
-- Indexen voor tabel `qcm`
--
ALTER TABLE `qcm`
  ADD PRIMARY KEY (`idqcm`),
  ADD KEY `idprof` (`idprof`);

--
-- Indexen voor tabel `qcm_user`
--
ALTER TABLE `qcm_user`
  ADD PRIMARY KEY (`iduser`,`idqcm`),
  ADD KEY `idqcm` (`idqcm`);

--
-- Indexen voor tabel `qst`
--
ALTER TABLE `qst`
  ADD PRIMARY KEY (`idqst`),
  ADD KEY `idqcm` (`idqcm`);

--
-- Indexen voor tabel `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`user_id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indexen voor tabel `user_rep`
--
ALTER TABLE `user_rep`
  ADD PRIMARY KEY (`idrepchoisite`),
  ADD KEY `idqst` (`idqst`),
  ADD KEY `idqcm` (`idqcm`);

--
-- AUTO_INCREMENT voor geëxporteerde tabellen
--

--
-- AUTO_INCREMENT voor een tabel `answer`
--
ALTER TABLE `answer`
  MODIFY `idanswer` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=38;

--
-- AUTO_INCREMENT voor een tabel `qcm`
--
ALTER TABLE `qcm`
  MODIFY `idqcm` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=27;

--
-- AUTO_INCREMENT voor een tabel `qst`
--
ALTER TABLE `qst`
  MODIFY `idqst` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=35;

--
-- AUTO_INCREMENT voor een tabel `users`
--
ALTER TABLE `users`
  MODIFY `user_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- Beperkingen voor geëxporteerde tabellen
--

--
-- Beperkingen voor tabel `answer`
--
ALTER TABLE `answer`
  ADD CONSTRAINT `answer_ibfk_1` FOREIGN KEY (`idqst`) REFERENCES `qst` (`idqst`);

--
-- Beperkingen voor tabel `qcm`
--
ALTER TABLE `qcm`
  ADD CONSTRAINT `qcm_ibfk_1` FOREIGN KEY (`idprof`) REFERENCES `users` (`user_id`);

--
-- Beperkingen voor tabel `qcm_user`
--
ALTER TABLE `qcm_user`
  ADD CONSTRAINT `qcm_user_ibfk_1` FOREIGN KEY (`iduser`) REFERENCES `users` (`user_id`),
  ADD CONSTRAINT `qcm_user_ibfk_2` FOREIGN KEY (`idqcm`) REFERENCES `qcm` (`idqcm`);

--
-- Beperkingen voor tabel `qst`
--
ALTER TABLE `qst`
  ADD CONSTRAINT `qst_ibfk_1` FOREIGN KEY (`idqcm`) REFERENCES `qcm` (`idqcm`);

--
-- Beperkingen voor tabel `user_rep`
--
ALTER TABLE `user_rep`
  ADD CONSTRAINT `user_rep_ibfk_1` FOREIGN KEY (`idqst`) REFERENCES `qst` (`idqst`),
  ADD CONSTRAINT `user_rep_ibfk_2` FOREIGN KEY (`idqcm`) REFERENCES `qcm` (`idqcm`);
COMMIT;
