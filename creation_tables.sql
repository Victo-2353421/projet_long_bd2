DROP DATABASE IF EXISTS `projet_long`;
CREATE DATABASE `projet_long` COLLATE utf8_unicode_ci;
USE `projet_long`;

CREATE TABLE `croutes` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nom` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
);

CREATE TABLE `sauces` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nom` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
);

CREATE TABLE `garnitures` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nom` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
);

CREATE TABLE `pizzas` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_croute` int NOT NULL,
  FOREIGN KEY (`id_croute`) REFERENCES `croutes` (`id`),
  PRIMARY KEY (`id`)
);

CREATE TABLE `sauces_pizzas` (
  `id_sauce` int NOT NULL,
  `id_pizza` int NOT NULL,
  FOREIGN KEY (`id_sauce`) REFERENCES `sauces` (`id`),
  FOREIGN KEY (`id_pizza`) REFERENCES `pizzas` (`id`)
);

CREATE TABLE `garnitures_pizzas` (
  `id_garniture` int NOT NULL,
  `id_pizza` int NOT NULL,
  FOREIGN KEY (`id_garniture`) REFERENCES `garnitures` (`id`),
  FOREIGN KEY (`id_pizza`) REFERENCES `pizzas` (`id`)
);

CREATE TABLE `clients` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nom` varchar(255) NOT NULL,
  `telephone` varchar(255) NOT NULL,
  `adresse` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
);

CREATE TABLE `commandes` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_pizza` int NOT NULL,
  `id_client` int NOT NULL,
  FOREIGN KEY (`id_pizza`) REFERENCES `pizzas` (`id`),
  FOREIGN KEY (`id_client`) REFERENCES `clients` (`id`),
  PRIMARY KEY (`id`)
);

CREATE TABLE `attente_commandes` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_commande` int NOT NULL,
  FOREIGN KEY (`id_commande`) REFERENCES `commandes` (`id`),
  PRIMARY KEY (`id`)
);

/**
 * Déclencheur pour la création d'une commande.
 * On ajoute la commande dans la liste d'attente.
 */
DELIMITER $$
CREATE TRIGGER `nouvelle_commande` AFTER INSERT ON `commandes` FOR EACH ROW
BEGIN
	INSERT INTO `attente_commandes` (`id_commande`) VALUES
		(NEW.id);
END $$
DELIMITER ;
