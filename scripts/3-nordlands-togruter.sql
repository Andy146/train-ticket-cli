--Operatør
INSERT INTO Operatør (navn) VALUES ("SJ Nord");

--Ukedager
INSERT INTO Ukedag (navn) VALUES ("Mandag");
INSERT INTO Ukedag (navn) VALUES ("Tirsdag");
INSERT INTO Ukedag (navn) VALUES ("Onsdag");
INSERT INTO Ukedag (navn) VALUES ("Torsdag");
INSERT INTO Ukedag (navn) VALUES ("Fredag");
INSERT INTO Ukedag (navn) VALUES ("Lørdag");
INSERT INTO Ukedag (navn) VALUES ("Søndag");

--Togrute
INSERT INTO Togrute (operatørID, strekningID) VALUES (1,1);
INSERT INTO Togrute (operatørID, strekningID) VALUES (1,1);
INSERT INTO Togrute (operatørID, strekningID) VALUES (1,1);

--KjørerPåDager
--Dagtog
INSERT INTO KjørerPåDag (ukedag, ruteID) VALUES ("Mandag", 1);
INSERT INTO KjørerPåDag (ukedag, ruteID) VALUES ("Tirsdag", 1);
INSERT INTO KjørerPåDag (ukedag, ruteID) VALUES ("Onsdag", 1);
INSERT INTO KjørerPåDag (ukedag, ruteID) VALUES ("Torsdag", 1);
INSERT INTO KjørerPåDag (ukedag, ruteID) VALUES ("Fredag", 1);

--Nattog
INSERT INTO KjørerPåDag (ukedag, ruteID) VALUES ("Mandag", 2);
INSERT INTO KjørerPåDag (ukedag, ruteID) VALUES ("Tirsdag", 2);
INSERT INTO KjørerPåDag (ukedag, ruteID) VALUES ("Onsdag", 2);
INSERT INTO KjørerPåDag (ukedag, ruteID) VALUES ("Torsdag", 2);
INSERT INTO KjørerPåDag (ukedag, ruteID) VALUES ("Fredag", 2);
INSERT INTO KjørerPåDag (ukedag, ruteID) VALUES ("Lørdag", 2);
INSERT INTO KjørerPåDag (ukedag, ruteID) VALUES ("Søndag", 2);

--Morgentog
INSERT INTO KjørerPåDag (ukedag, ruteID) VALUES ("Mandag", 3);
INSERT INTO KjørerPåDag (ukedag, ruteID) VALUES ("Tirsdag", 3);
INSERT INTO KjørerPåDag (ukedag, ruteID) VALUES ("Onsdag", 3);
INSERT INTO KjørerPåDag (ukedag, ruteID) VALUES ("Torsdag", 3);
INSERT INTO KjørerPåDag (ukedag, ruteID) VALUES ("Fredag", 3);


--Vogntyper
INSERT INTO Vogntype (navn, operatørID) VALUES ("SJ-sittevogn-1", 1);
INSERT INTO Vogntype (navn, operatørID) VALUES ("SJ-sovevogn-1", 1);

INSERT INTO Sittevogn (typeID, seteRader, seteKolonner) VALUES (1,3,4);
INSERT INTO Sovevogn (typeID, antallKupeer) VALUES (2,4);

--Vogner
--Dagtog vogner
INSERT INTO Vogn (typeID) VALUES (1);
INSERT INTO Vogn (typeID) VALUES (1);

--Nattog vogner
INSERT INTO Vogn (typeID) VALUES (1);
INSERT INTO Vogn (typeID) VALUES (2);

--Morgentog vogner
INSERT INTO Vogn (typeID) VALUES (1);


--VognOppsett
--Dagtog
INSERT INTO VognOppsett (ruteID, vognID, vognnummer) VALUES (1,1,1);
INSERT INTO VognOppsett (ruteID, vognID, vognnummer) VALUES (1,2,2);

--Nattog
INSERT INTO VognOppsett (ruteID, vognID, vognnummer) VALUES (2,3,1);
INSERT INTO VognOppsett (ruteID, vognID, vognnummer) VALUES (2,4,2);

--Morgentog
INSERT INTO VognOppsett (ruteID, vognID, vognnummer) VALUES (3,5,1);



--Rutetabell
--Dagtog rute
INSERT INTO Rutetabell (ruteID, stasjonNavn, avreise,neste_dag) VALUES (1,"Trondheim S", "07:49", FALSE);
INSERT INTO Rutetabell (ruteID, stasjonNavn, ankomst, avreise,neste_dag) VALUES (1,"Steinkjer", "09:51", "09:51", FALSE);
INSERT INTO Rutetabell (ruteID, stasjonNavn, ankomst, avreise,neste_dag) VALUES (1,"Mosjøen", "13:20", "13:20", FALSE);
INSERT INTO Rutetabell (ruteID, stasjonNavn, ankomst, avreise,neste_dag) VALUES (1,"Mo i Rana", "14:31", "14:31", FALSE);
INSERT INTO Rutetabell (ruteID, stasjonNavn, ankomst, avreise,neste_dag) VALUES (1,"Fauske", "16:49", "16:49", FALSE);
INSERT INTO Rutetabell (ruteID, stasjonNavn, ankomst,neste_dag) VALUES (1,"Bodø", "17:34", FALSE);

--Nattog rute
INSERT INTO Rutetabell (ruteID, stasjonNavn, avreise, neste_dag) VALUES (2,"Trondheim S", "23:05", FALSE);
INSERT INTO Rutetabell (ruteID, stasjonNavn, ankomst, avreise, neste_dag) VALUES (2,"Steinkjer", "00:57", "00:57", TRUE);
INSERT INTO Rutetabell (ruteID, stasjonNavn, ankomst, avreise,neste_dag) VALUES (2,"Mosjøen", "04:41", "04:41", TRUE);
INSERT INTO Rutetabell (ruteID, stasjonNavn, ankomst, avreise, neste_dag) VALUES (2,"Mo i Rana", "05:55", "05:55", TRUE);
INSERT INTO Rutetabell (ruteID, stasjonNavn, ankomst, avreise, neste_dag) VALUES (2,"Fauske", "08:19", "08:19", TRUE);
INSERT INTO Rutetabell (ruteID, stasjonNavn, ankomst, neste_dag) VALUES (2,"Bodø", "09:05", TRUE);

--Morgentog rute
INSERT INTO Rutetabell (ruteID, stasjonNavn, avreise,neste_dag) VALUES (3,"Mo i Rana", "08:11", FALSE);
INSERT INTO Rutetabell (ruteID, stasjonNavn, ankomst, avreise,neste_dag) VALUES (3,"Mosjøen", "09:14", "09:14", FALSE);
INSERT INTO Rutetabell (ruteID, stasjonNavn, ankomst, avreise,neste_dag) VALUES (3,"Steinkjer", "12:31", "12:31", FALSE);
INSERT INTO Rutetabell (ruteID, stasjonNavn, ankomst,neste_dag) VALUES (3,"Trondheim S", "14:13", FALSE);


--Seter og kupeer
INSERT INTO Sete (vognID, setenummer) VALUES (1,1);
INSERT INTO Sete (vognID, setenummer) VALUES (1,2);
INSERT INTO Sete (vognID, setenummer) VALUES (1,3);
INSERT INTO Sete (vognID, setenummer) VALUES (1,4);
INSERT INTO Sete (vognID, setenummer) VALUES (1,5);
INSERT INTO Sete (vognID, setenummer) VALUES (1,6);
INSERT INTO Sete (vognID, setenummer) VALUES (1,7);
INSERT INTO Sete (vognID, setenummer) VALUES (1,8);
INSERT INTO Sete (vognID, setenummer) VALUES (1,9);
INSERT INTO Sete (vognID, setenummer) VALUES (1,10);
INSERT INTO Sete (vognID, setenummer) VALUES (1,11);
INSERT INTO Sete (vognID, setenummer) VALUES (1,12);

INSERT INTO Sete (vognID, setenummer) VALUES (2,1);
INSERT INTO Sete (vognID, setenummer) VALUES (2,2);
INSERT INTO Sete (vognID, setenummer) VALUES (2,3);
INSERT INTO Sete (vognID, setenummer) VALUES (2,4);
INSERT INTO Sete (vognID, setenummer) VALUES (2,5);
INSERT INTO Sete (vognID, setenummer) VALUES (2,6);
INSERT INTO Sete (vognID, setenummer) VALUES (2,7);
INSERT INTO Sete (vognID, setenummer) VALUES (2,8);
INSERT INTO Sete (vognID, setenummer) VALUES (2,9);
INSERT INTO Sete (vognID, setenummer) VALUES (2,10);
INSERT INTO Sete (vognID, setenummer) VALUES (2,11);
INSERT INTO Sete (vognID, setenummer) VALUES (2,12);

INSERT INTO Sete (vognID, setenummer) VALUES (3,1);
INSERT INTO Sete (vognID, setenummer) VALUES (3,2);
INSERT INTO Sete (vognID, setenummer) VALUES (3,3);
INSERT INTO Sete (vognID, setenummer) VALUES (3,4);
INSERT INTO Sete (vognID, setenummer) VALUES (3,5);
INSERT INTO Sete (vognID, setenummer) VALUES (3,6);
INSERT INTO Sete (vognID, setenummer) VALUES (3,7);
INSERT INTO Sete (vognID, setenummer) VALUES (3,8);
INSERT INTO Sete (vognID, setenummer) VALUES (3,9);
INSERT INTO Sete (vognID, setenummer) VALUES (3,10);
INSERT INTO Sete (vognID, setenummer) VALUES (3,11);
INSERT INTO Sete (vognID, setenummer) VALUES (3,12);

INSERT INTO Kupee (vognID, kupeenummer) VALUES (4,1);
INSERT INTO Kupee (vognID, kupeenummer) VALUES (4,2);
INSERT INTO Kupee (vognID, kupeenummer) VALUES (4,3);
INSERT INTO Kupee (vognID, kupeenummer) VALUES (4,4);

INSERT INTO Sete (vognID, setenummer) VALUES (5,1);
INSERT INTO Sete (vognID, setenummer) VALUES (5,2);
INSERT INTO Sete (vognID, setenummer) VALUES (5,3);
INSERT INTO Sete (vognID, setenummer) VALUES (5,4);
INSERT INTO Sete (vognID, setenummer) VALUES (5,5);
INSERT INTO Sete (vognID, setenummer) VALUES (5,6);
INSERT INTO Sete (vognID, setenummer) VALUES (5,7);
INSERT INTO Sete (vognID, setenummer) VALUES (5,8);
INSERT INTO Sete (vognID, setenummer) VALUES (5,9);
INSERT INTO Sete (vognID, setenummer) VALUES (5,10);
INSERT INTO Sete (vognID, setenummer) VALUES (5,11);
INSERT INTO Sete (vognID, setenummer) VALUES (5,12);
