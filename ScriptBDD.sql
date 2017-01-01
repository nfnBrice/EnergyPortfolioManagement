#weird : data type float not accepted so use of decimal but not optimum. 

DROP DATABASE IF EXISTS ma_base ;
CREATE DATABASE IF NOT EXISTS ma_base;
USE ma_base;

# DATABASE SETUP

CREATE TABLE Users(
    UserID INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    Mail VARCHAR(100),
    Pseudo VARCHAR(100),
    Mdp VARCHAR(250)
    );

CREATE TABLE Portfolio(
    PortfolioID INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    Amount decimal,
    Horizon DATE,
    UserID INT, 
    FOREIGN KEY (UserID) REFERENCES Users (UserID)
    );

CREATE TABLE Bond(
    BondID INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    Issue VARCHAR (250),
    Country VARCHAR(50),
    Issuer VARCHAR (100),
    Currency VARCHAR(3),
    Status VARCHAR(30),
    Coupon decimal,
    Issue_amount int,
    USD_equivalent int,
    Nominal int,
    Outstanding_value int, 
    ISIN VARCHAR(20),
    Start_of_placement DATE,
    End_of_placement DATE,
    Maturity DATE,
    Foreign_rating VARCHAR(30),
    Local_rating VARCHAR(30),
    Stock_exchange VARCHAR(50),
    Trade_date DATE,
    Indicative_price decimal,
    Effective_yield decimal,
    Duration decimal,
    Vector_image VARCHAR(10000),
    #Profit INT,
    #Period VARCHAR(30),
    #Parvalue VARCHAR(30),
    PortfolioID int,
    FOREIGN KEY (PortfolioID) REFERENCES Portfolio(PortfolioID)
    );

CREATE TABLE Stock(
    StockID INT NOT NULL PRIMARY KEY AUTO_INCREMENT, 
    Type VARCHAR(1)
    );

CREATE TABLE Project(
    ProjectID INT NOT NULL PRIMARY KEY AUTO_INCREMENT, 
    Type VARCHAR(1)
    );

CREATE TABLE PortfolioLink(
    PortfolioLinkID INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    Quantity INT,
    Type VARCHAR(30),
    PortfolioID INT,
    BondID INT,
    StockID INT,
    ProjectID INT,
    FOREIGN KEY (PortfolioID) REFERENCES Portfolio(PortfolioID),
    FOREIGN KEY (BondID) REFERENCES Bond(BondID),
    FOREIGN KEY (StockID) REFERENCES Stock(StockID),
    FOREIGN KEY (ProjectID) REFERENCES Project(ProjectID)
    );

CREATE TABLE Pricehistory(
    PriceHistoryID INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    Price decimal ,
    PriceTime DATE ,
    BondID INT NOT NULL,
    FOREIGN KEY (BondID) REFERENCES Bond(BondID) 
    );


# STORED PROCEDURES SETUP

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_createUser`(
    IN p_mail VARCHAR(100),
    IN p_pseudo VARCHAR(100),
    IN p_mdp VARCHAR(250)
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
                    Mail,
                    Pseudo,
                    Mdp
                )
                values
                (
                    p_mail,
                    p_pseudo,
                    p_mdp
                );
            END IF;
        END IF;
    END$$
    DELIMITER ;

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_connect`
    (
        IN p_mail VARCHAR(100)
    )

    BEGIN
        select * from Users where Mail = p_mail;
    END$$
    DELIMITER ;

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_createPortfolio`(
    IN p_amount decimal,
    IN p_horizon decimal,
    IN p_userIDs INT(250)
    )
    BEGIN
             
                insert into Portfolio
                (
                    Amount,
                    Horizon,
                    UserID
                )
                values
                (
                    p_amount,
                    p_horizon,
                    p_userIDs
                );
    END$$
    DELIMITER ;

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_addBondToPortfolio`(
    IN p_BondID int,
    IN p_PortfolioID int,
    IN p_Quantity INT
    )
    BEGIN
             
        insert into BondPortfolioLink
        (
            BondID,
            PortfolioID,
            Quantity
        )
        values
        (
            p_BondID,
            p_PortfolioID,
            p_Quantity
        );
    END$$
    DELIMITER ;
