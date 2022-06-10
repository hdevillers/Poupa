-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1:3306
-- Généré le : ven. 10 juin 2022 à 15:34
-- Version du serveur : 5.7.36
-- Version de PHP : 7.4.26

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `poupa`
--

-- --------------------------------------------------------

--
-- Structure de la table `boitiers`
--

DROP TABLE IF EXISTS `boitiers`;
CREATE TABLE IF NOT EXISTS `boitiers` (
  `id` int(9) NOT NULL AUTO_INCREMENT,
  `numeros` int(3) NOT NULL,
  `proprietaire` varchar(20) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  KEY `fk_boitier_proprio` (`proprietaire`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

--
-- Déchargement des données de la table `boitiers`
--

INSERT INTO `boitiers` (`id`, `numeros`, `proprietaire`) VALUES
(1, 1, 'mrakowski'),
(2, 2, 'mrakowski');

-- --------------------------------------------------------

--
-- Structure de la table `capteurs`
--

DROP TABLE IF EXISTS `capteurs`;
CREATE TABLE IF NOT EXISTS `capteurs` (
  `numeros` int(11) NOT NULL,
  `id_experience` varchar(50) NOT NULL,
  `alias` varchar(50) NOT NULL,
  `id_farine` int(3) DEFAULT NULL,
  `id_levain` int(11) DEFAULT NULL,
  `levure` varchar(50) DEFAULT NULL,
  `remarque` varchar(100) DEFAULT NULL,
  `fichier_donnees` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`numeros`,`id_experience`) USING BTREE,
  UNIQUE KEY `unique_id` (`alias`,`id_experience`) USING BTREE,
  KEY `fk_utCpt_exp` (`id_experience`),
  KEY `fk_cpt_farine` (`id_farine`),
  KEY `fk_cpt_levain` (`id_levain`),
  KEY `fk_cpt_levure` (`levure`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Déchargement des données de la table `capteurs`
--

INSERT INTO `capteurs` (`numeros`, `id_experience`, `alias`, `id_farine`, `id_levain`, `levure`, `remarque`, `fichier_donnees`) VALUES
(1, '1_2022-06-07_mrakowski', 'Capteur_1', NULL, NULL, NULL, 'None', '2_2022-06-07_mrakowski_Capteur-1.csv'),
(1, '2_2022-06-10_mrakowski', 'a', NULL, NULL, NULL, 'None', '2_2022-06-10_mrakowski_Capteur-1.csv'),
(2, '1_2022-06-07_mrakowski', 'Capteur_2', NULL, NULL, NULL, 'None', '2_2022-06-07_mrakowski_Capteur-2.csv'),
(2, '2_2022-06-10_mrakowski', 'b', NULL, NULL, NULL, 'None', '2_2022-06-10_mrakowski_Capteur-2.csv'),
(3, '1_2022-06-07_mrakowski', 'Capteur_3', NULL, NULL, NULL, 'None', '2_2022-06-07_mrakowski_Capteur-3.csv'),
(3, '2_2022-06-10_mrakowski', 'c', NULL, NULL, NULL, 'None', '2_2022-06-10_mrakowski_Capteur-3.csv'),
(4, '1_2022-06-07_mrakowski', 'Capteur_4', NULL, NULL, NULL, 'None', '2_2022-06-07_mrakowski_Capteur-4.csv'),
(4, '2_2022-06-10_mrakowski', 'd', NULL, NULL, NULL, 'None', '2_2022-06-10_mrakowski_Capteur-4.csv');

-- --------------------------------------------------------

--
-- Structure de la table `experiences`
--

DROP TABLE IF EXISTS `experiences`;
CREATE TABLE IF NOT EXISTS `experiences` (
  `id` varchar(50) NOT NULL,
  `projet` varchar(50) DEFAULT NULL,
  `id_boitier` int(10) NOT NULL,
  `operateur` varchar(20) NOT NULL,
  `date` date NOT NULL,
  `lieu` varchar(50) NOT NULL,
  `fichier_donnees` varchar(50) NOT NULL,
  `fichier_resultat` varchar(50) DEFAULT NULL,
  `remarque` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_exp_op` (`operateur`),
  KEY `fk_exp_pro` (`projet`),
  KEY `fk_exp_b` (`id_boitier`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Déchargement des données de la table `experiences`
--

INSERT INTO `experiences` (`id`, `projet`, `id_boitier`, `operateur`, `date`, `lieu`, `fichier_donnees`, `fichier_resultat`, `remarque`) VALUES
('1_2022-06-07_mrakowski', NULL, 1, 'mrakowski', '2022-06-07', 'Montpellier', 'PP01-001.TXT', 'files/1_2022-06-07_mrakowski.TXT', NULL),
('2_2022-06-10_mrakowski', 'mrakowski_Un projet Hyper cool', 2, 'mrakowski', '2022-06-10', 'Montpellier', 'PP02-001.TXT', 'files/2_2022-06-10_mrakowski.TXT', NULL);

-- --------------------------------------------------------

--
-- Structure de la table `farines`
--

DROP TABLE IF EXISTS `farines`;
CREATE TABLE IF NOT EXISTS `farines` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `alias` varchar(50) DEFAULT NULL,
  `cereale` varchar(50) DEFAULT NULL,
  `type_mouture` varchar(50) DEFAULT NULL,
  `cendre` varchar(50) DEFAULT NULL,
  `origine` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

--
-- Déchargement des données de la table `farines`
--

INSERT INTO `farines` (`id`, `alias`, `cereale`, `type_mouture`, `cendre`, `origine`) VALUES
(1, 'Farine expérimentale 75 ', 'blé', '', '', 'Inrae');

-- --------------------------------------------------------

--
-- Structure de la table `levains`
--

DROP TABLE IF EXISTS `levains`;
CREATE TABLE IF NOT EXISTS `levains` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `alias` varchar(50) DEFAULT NULL,
  `farine` int(11) DEFAULT NULL,
  `origine` varchar(100) DEFAULT NULL,
  `cereale` varchar(50) DEFAULT NULL,
  `hydratation` int(3) DEFAULT NULL,
  `microbiome` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_id` (`id`),
  KEY `fk_levain_farine` (`farine`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

--
-- Déchargement des données de la table `levains`
--

INSERT INTO `levains` (`id`, `alias`, `farine`, `origine`, `cereale`, `hydratation`, `microbiome`) VALUES
(1, 'levain pouette', 1, 'INRAe', '', 0, ''),
(2, '', 1, '', '', NULL, 'Ya de superbes microorganismes'),
(3, 'un autre levain', 1, '', '', 46, '');

-- --------------------------------------------------------

--
-- Structure de la table `levures`
--

DROP TABLE IF EXISTS `levures`;
CREATE TABLE IF NOT EXISTS `levures` (
  `espece` varchar(50) NOT NULL,
  `origine` varchar(50) NOT NULL,
  PRIMARY KEY (`espece`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Déchargement des données de la table `levures`
--

INSERT INTO `levures` (`espece`, `origine`) VALUES
('une levure vraiment stylé', 'INRAe'),
('Youhou', 'Ici la vie est belle');

-- --------------------------------------------------------

--
-- Structure de la table `participer_projet`
--

DROP TABLE IF EXISTS `participer_projet`;
CREATE TABLE IF NOT EXISTS `participer_projet` (
  `id_projet` varchar(50) NOT NULL,
  `login_utilisateur` varchar(20) NOT NULL,
  PRIMARY KEY (`id_projet`,`login_utilisateur`),
  KEY `fk_participer_user` (`login_utilisateur`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Déchargement des données de la table `participer_projet`
--

INSERT INTO `participer_projet` (`id_projet`, `login_utilisateur`) VALUES
('mrakowski_Un projet Hyper cool', 'fmabille'),
('mrakowski_Un projet Hyper cool', 'mrakowski'),
('mrakowski_Un projet Hyper cool', 'sdequin');

-- --------------------------------------------------------

--
-- Structure de la table `projets`
--

DROP TABLE IF EXISTS `projets`;
CREATE TABLE IF NOT EXISTS `projets` (
  `id` varchar(50) NOT NULL,
  `titre` varchar(50) NOT NULL,
  `directeur` varchar(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_projet_dir` (`directeur`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Déchargement des données de la table `projets`
--

INSERT INTO `projets` (`id`, `titre`, `directeur`) VALUES
('mrakowski_Un projet Hyper cool', 'Un projet Hyper cool', 'mrakowski');

-- --------------------------------------------------------

--
-- Structure de la table `users`
--

DROP TABLE IF EXISTS `users`;
CREATE TABLE IF NOT EXISTS `users` (
  `login` varchar(20) NOT NULL,
  `nom` varchar(20) NOT NULL,
  `prenom` varchar(20) NOT NULL,
  `mot_de_passe` varchar(64) NOT NULL,
  PRIMARY KEY (`login`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Déchargement des données de la table `users`
--

INSERT INTO `users` (`login`, `nom`, `prenom`, `mot_de_passe`) VALUES
('fmabille', 'frédéric', 'mabille', '22b347fb0391ea74dbdf2f93b1ea5d5fe58a04b8f04d76026c733d99d9f826f9'),
('mrakowski', 'rakowski', 'maelis', '2fa85dd42ff469fd28b52b1d19411158138b14803cf98d30803c1d61a8dc0677'),
('sdequin', 'Dequin', 'Sylvie', 'ad8b9a6c04e5b94e6fed77699ce3c47772e6900894db72ffd6afafc5ae7a6cb3');

--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `boitiers`
--
ALTER TABLE `boitiers`
  ADD CONSTRAINT `fk_boitier_proprio` FOREIGN KEY (`proprietaire`) REFERENCES `users` (`login`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Contraintes pour la table `capteurs`
--
ALTER TABLE `capteurs`
  ADD CONSTRAINT `fk_cpt_farine` FOREIGN KEY (`id_farine`) REFERENCES `farines` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_cpt_levain` FOREIGN KEY (`id_levain`) REFERENCES `levains` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_cpt_levure` FOREIGN KEY (`levure`) REFERENCES `levures` (`espece`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_utCpt_exp` FOREIGN KEY (`id_experience`) REFERENCES `experiences` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Contraintes pour la table `experiences`
--
ALTER TABLE `experiences`
  ADD CONSTRAINT `fk_exp_b` FOREIGN KEY (`id_boitier`) REFERENCES `boitiers` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_exp_op` FOREIGN KEY (`operateur`) REFERENCES `users` (`login`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_exp_pro` FOREIGN KEY (`projet`) REFERENCES `projets` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Contraintes pour la table `levains`
--
ALTER TABLE `levains`
  ADD CONSTRAINT `fk_levain_farine` FOREIGN KEY (`farine`) REFERENCES `farines` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Contraintes pour la table `participer_projet`
--
ALTER TABLE `participer_projet`
  ADD CONSTRAINT `fk_participer_projet` FOREIGN KEY (`id_projet`) REFERENCES `projets` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_participer_user` FOREIGN KEY (`login_utilisateur`) REFERENCES `users` (`login`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Contraintes pour la table `projets`
--
ALTER TABLE `projets`
  ADD CONSTRAINT `fk_projet_dir` FOREIGN KEY (`directeur`) REFERENCES `users` (`login`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
