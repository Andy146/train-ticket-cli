--Stasjoner
INSERT INTO Stasjon (navn, moh) VALUES ("Bodø", 4.1);
INSERT INTO Stasjon (navn, moh) VALUES ("Fauske",34.0);
INSERT INTO Stasjon (navn, moh) VALUES ("Mo i Rana", 3.5);
INSERT INTO Stasjon (navn, moh) VALUES ("Mosjøen", 6.8);
INSERT INTO Stasjon (navn, moh) VALUES ("Steinkjer", 3.6);
INSERT INTO Stasjon (navn, moh) VALUES ("Trondheim S", 5.1);

--Banestrekning
INSERT INTO Banestrekning (navn, energiType, start, ende) VALUES ("Nordlandsbanen", "diesel", "Trondheim S", "Bodø");

--Delstrekninger
INSERT INTO Delstrekning (stasjonA, stasjonB, distanse, dobbeltSpor, strekningID) VALUES ("Trondheim S", "Steinkjer", 120, TRUE, 1);
INSERT INTO Delstrekning (stasjonA, stasjonB, distanse, dobbeltSpor, strekningID) VALUES ("Steinkjer", "Mosjøen", 280, FALSE, 1);
INSERT INTO Delstrekning (stasjonA, stasjonB, distanse, dobbeltSpor, strekningID) VALUES ("Mosjøen", "Mo i Rana", 90, FALSE, 1);
INSERT INTO Delstrekning (stasjonA, stasjonB, distanse, dobbeltSpor, strekningID) VALUES ("Mo i Rana", "Fauske", 170, FALSE, 1);
INSERT INTO Delstrekning (stasjonA, stasjonB, distanse, dobbeltSpor, strekningID) VALUES ("Fauske", "Bodø", 60, FALSE, 1);
