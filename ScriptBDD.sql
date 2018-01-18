DROP DATABASE IF EXISTS ma_bases ;
CREATE DATABASE IF NOT EXISTS ma_bases;
USE ma_bases;


CREATE TABLE Bond(
BondID INT PRIMARY KEY NOT NULL AUTO_INCREMENT ,
Name VARCHAR (30),
Issuer VARCHAR (30),
Profit INT ,
Maturity DOUBLE,
Period VARCHAR(30),
Parvalue VARCHAR(30),
Couponrate VARCHAR(30),
MacaulayDuration DOUBLE
);


CREATE TABLE Portfolio(
PortfolioID INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
BondID INT NOT NULL,
FOREIGN KEY (BondID) REFERENCES Bond(BondID) 
);

CREATE TABLE Pricehistory(
PriceHistoryID INT NOT NULL PRIMARY KEY AUTO_INCREMENT ,
Price DOUBLE ,
PriceTime DATE ,
BondID INT NOT NULL,
FOREIGN KEY (BondID) REFERENCES Bond(BondID) 
);

CREATE TABLE Stock(
StockID INT NOT NULL PRIMARY KEY AUTO_INCREMENT, 
Type VARCHAR(1)
);

CREATE TABLE Users(
UserID INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
Mail VARCHAR(100),
Pseudo VARCHAR(100),
Mdp VARCHAR(10),
PortfolioID INT,
FOREIGN KEY (PortfolioID) REFERENCES Portfolio(PortfolioID)
);


DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_createUser`(
    IN p_mail VARCHAR(100),
    IN p_pseudo VARCHAR(100),
    IN p_mdp VARCHAR(10)
)
BEGIN
    if ( select exists (select 1 from Users where Pseudo = p_pseudo) ) THEN
     
        select 'Username Exists !!';

    ELSE
        if ( select exists (select 1 from Users where Mail = p_mail) ) THEN
        select 'You already have an account !!';
     
        ELSE
         
            insert into Users
            (
                Pseudo,
                Mail,
                Mdp
            )
            values
            (
                p_pseudo,
                p_mail,
                p_mdp
            );
        END IF;
    END IF;
END$$
DELIMITER ;

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_connect`
(
    IN p_username VARCHAR(100)
)

BEGIN
    select * from tbl_user where user_username = p_username;
END$$
DELIMITER ;