USE `projet_long`;

INSERT INTO `croutes` (`nom`) VALUES
("Classique"),
("Mince"),
("Épaisse");

INSERT INTO `sauces` (`nom`) VALUES
("Tomate"),
("Spaghetti"),
("Alfredo");

INSERT INTO `garnitures` (`nom`) VALUES
("Pepperoni"),
("Champignons"),
("Oignons"),
("Poivrons"),
("Olives"),
("Anchois"),
("Bacon"),
("Poulet"),
("Maïs"),
("Fromage"),
("Piments forts");

INSERT INTO `clients` (`nom`, `telephone`, `adresse`) VALUES
("Gertrude Gagné", "8191231234", "2 rue Patente Victoriaville"),
("Olivier Dumont", "3745833443", "9 rue Bidon Chibougamau"),
("Michel Tremblay", "9724812748", "12 rue Chose Ville");

INSERT INTO `pizzas` (`id_croute`) VALUES
(2);
INSERT INTO `sauces_pizzas` (`id_sauce`, `id_pizza`) VALUES
(3, 1);
INSERT INTO `garniture_pizzas` (`id_garniture`, `id_pizza`) VALUES
(5, 1);
INSERT INTO `garniture_pizzas` (`id_garniture`, `id_pizza`) VALUES
(1, 1);

INSERT INTO `commandes` (`id_pizza`, `id_client`) VALUES
(1, 1);