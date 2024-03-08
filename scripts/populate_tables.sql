INSERT INTO PUBLISH (PUBLISHER_NAME) VALUES 
('Electronic Arts'),
('Ubisoft'),
('CD Projekt Red'),
('Rockstar Games'),
('Square Enix');

INSERT INTO GAMES (GAME_NAME, PRICE, STOCK, RELEASE_DATE, PID, GAME_DESCRIPTION) VALUES
('FIFA 22', 59, 1000, '2021-10-01', 1, 'The latest installment in the popular football simulation series.'),
('Assassins Creed Odyssey', 49, 800, '2018-10-05', 2, 'Embark on a journey to ancient Greece in this action RPG.'),
('Cyberpunk 2077', 55, 1200, '2020-12-10', 3, 'Explore the futuristic Night City in this open-world RPG.'),
('Grand Theft Auto V', 29, 1540, '2013-09-17', 4, 'An open-world action-adventure game set in the fictional state of San Andreas.'),
('Red Dead Redemption 2', 59, 6100, '2018-10-26', 4, 'An epic tale of life in America at the dawn of the modern age.');

INSERT INTO CLIENTS (USRNME, PASSWRD, isADM) VALUES 
('johndoe', 'password123', 0),
('alicesmith', 'securepass', 0),
('adminuser', 'adminpass', 1),
('evamiller', 'eva123456', 0),
('charliedavis', 'charliepass', 0);

INSERT INTO CONTACT (CID, PNUMBER, EMAIL) VALUES 
(1, '0712345678', 'john.doe@example.com'),
(2, '0723456789', 'alice.smith@example.com'),
(3, '0711111111', 'admin@example.com'),
(4, '0745678901', 'eva.miller@example.com'),
(5, '0756789012', 'charlie.davis@example.com');

INSERT INTO ORDERS (CID, GID) VALUES 
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5);