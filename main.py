from components.text_to_sql_pipeline import TextToSQLPipeline

# Descrição do schema
schema_description = """
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema chinook
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema chinook
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `chinook` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
USE `chinook` ;

-- -----------------------------------------------------
-- Table `chinook`.`artist`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `chinook`.`artist` (
  `ArtistId` INT NOT NULL,
  `Name` VARCHAR(120) CHARACTER SET 'utf8mb3' NULL DEFAULT NULL,
  PRIMARY KEY (`ArtistId`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `chinook`.`album`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `chinook`.`album` (
  `AlbumId` INT NOT NULL,
  `Title` VARCHAR(160) CHARACTER SET 'utf8mb3' NOT NULL,
  `ArtistId` INT NOT NULL,
  PRIMARY KEY (`AlbumId`),
  INDEX `IFK_AlbumArtistId` (`ArtistId` ASC) VISIBLE,
  CONSTRAINT `FK_AlbumArtistId`
    FOREIGN KEY (`ArtistId`)
    REFERENCES `chinook`.`artist` (`ArtistId`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `chinook`.`employee`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `chinook`.`employee` (
  `EmployeeId` INT NOT NULL,
  `LastName` VARCHAR(20) CHARACTER SET 'utf8mb3' NOT NULL,
  `FirstName` VARCHAR(20) CHARACTER SET 'utf8mb3' NOT NULL,
  `Title` VARCHAR(30) CHARACTER SET 'utf8mb3' NULL DEFAULT NULL,
  `ReportsTo` INT NULL DEFAULT NULL,
  `BirthDate` DATETIME NULL DEFAULT NULL,
  `HireDate` DATETIME NULL DEFAULT NULL,
  `Address` VARCHAR(70) CHARACTER SET 'utf8mb3' NULL DEFAULT NULL,
  `City` VARCHAR(40) CHARACTER SET 'utf8mb3' NULL DEFAULT NULL,
  `State` VARCHAR(40) CHARACTER SET 'utf8mb3' NULL DEFAULT NULL,
  `Country` VARCHAR(40) CHARACTER SET 'utf8mb3' NULL DEFAULT NULL,
  `PostalCode` VARCHAR(10) CHARACTER SET 'utf8mb3' NULL DEFAULT NULL,
  `Phone` VARCHAR(24) CHARACTER SET 'utf8mb3' NULL DEFAULT NULL,
  `Fax` VARCHAR(24) CHARACTER SET 'utf8mb3' NULL DEFAULT NULL,
  `Email` VARCHAR(60) CHARACTER SET 'utf8mb3' NULL DEFAULT NULL,
  PRIMARY KEY (`EmployeeId`),
  INDEX `IFK_EmployeeReportsTo` (`ReportsTo` ASC) VISIBLE,
  CONSTRAINT `FK_EmployeeReportsTo`
    FOREIGN KEY (`ReportsTo`)
    REFERENCES `chinook`.`employee` (`EmployeeId`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `chinook`.`customer`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `chinook`.`customer` (
  `CustomerId` INT NOT NULL,
  `FirstName` VARCHAR(40) CHARACTER SET 'utf8mb3' NOT NULL,
  `LastName` VARCHAR(20) CHARACTER SET 'utf8mb3' NOT NULL,
  `Company` VARCHAR(80) CHARACTER SET 'utf8mb3' NULL DEFAULT NULL,
  `Address` VARCHAR(70) CHARACTER SET 'utf8mb3' NULL DEFAULT NULL,
  `City` VARCHAR(40) CHARACTER SET 'utf8mb3' NULL DEFAULT NULL,
  `State` VARCHAR(40) CHARACTER SET 'utf8mb3' NULL DEFAULT NULL,
  `Country` VARCHAR(40) CHARACTER SET 'utf8mb3' NULL DEFAULT NULL,
  `PostalCode` VARCHAR(10) CHARACTER SET 'utf8mb3' NULL DEFAULT NULL,
  `Phone` VARCHAR(24) CHARACTER SET 'utf8mb3' NULL DEFAULT NULL,
  `Fax` VARCHAR(24) CHARACTER SET 'utf8mb3' NULL DEFAULT NULL,
  `Email` VARCHAR(60) CHARACTER SET 'utf8mb3' NOT NULL,
  `SupportRepId` INT NULL DEFAULT NULL,
  PRIMARY KEY (`CustomerId`),
  INDEX `IFK_CustomerSupportRepId` (`SupportRepId` ASC) VISIBLE,
  CONSTRAINT `FK_CustomerSupportRepId`
    FOREIGN KEY (`SupportRepId`)
    REFERENCES `chinook`.`employee` (`EmployeeId`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `chinook`.`genre`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `chinook`.`genre` (
  `GenreId` INT NOT NULL,
  `Name` VARCHAR(120) CHARACTER SET 'utf8mb3' NULL DEFAULT NULL,
  PRIMARY KEY (`GenreId`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `chinook`.`invoice`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `chinook`.`invoice` (
  `InvoiceId` INT NOT NULL,
  `CustomerId` INT NOT NULL,
  `InvoiceDate` DATETIME NOT NULL,
  `BillingAddress` VARCHAR(70) CHARACTER SET 'utf8mb3' NULL DEFAULT NULL,
  `BillingCity` VARCHAR(40) CHARACTER SET 'utf8mb3' NULL DEFAULT NULL,
  `BillingState` VARCHAR(40) CHARACTER SET 'utf8mb3' NULL DEFAULT NULL,
  `BillingCountry` VARCHAR(40) CHARACTER SET 'utf8mb3' NULL DEFAULT NULL,
  `BillingPostalCode` VARCHAR(10) CHARACTER SET 'utf8mb3' NULL DEFAULT NULL,
  `Total` DECIMAL(10,2) NOT NULL,
  PRIMARY KEY (`InvoiceId`),
  INDEX `IFK_InvoiceCustomerId` (`CustomerId` ASC) VISIBLE,
  CONSTRAINT `FK_InvoiceCustomerId`
    FOREIGN KEY (`CustomerId`)
    REFERENCES `chinook`.`customer` (`CustomerId`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `chinook`.`mediatype`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `chinook`.`mediatype` (
  `MediaTypeId` INT NOT NULL,
  `Name` VARCHAR(120) CHARACTER SET 'utf8mb3' NULL DEFAULT NULL,
  PRIMARY KEY (`MediaTypeId`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `chinook`.`track`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `chinook`.`track` (
  `TrackId` INT NOT NULL,
  `Name` VARCHAR(200) CHARACTER SET 'utf8mb3' NOT NULL,
  `AlbumId` INT NULL DEFAULT NULL,
  `MediaTypeId` INT NOT NULL,
  `GenreId` INT NULL DEFAULT NULL,
  `Composer` VARCHAR(220) CHARACTER SET 'utf8mb3' NULL DEFAULT NULL,
  `Milliseconds` INT NOT NULL,
  `Bytes` INT NULL DEFAULT NULL,
  `UnitPrice` DECIMAL(10,2) NOT NULL,
  PRIMARY KEY (`TrackId`),
  INDEX `IFK_TrackAlbumId` (`AlbumId` ASC) VISIBLE,
  INDEX `IFK_TrackGenreId` (`GenreId` ASC) VISIBLE,
  INDEX `IFK_TrackMediaTypeId` (`MediaTypeId` ASC) VISIBLE,
  CONSTRAINT `FK_TrackAlbumId`
    FOREIGN KEY (`AlbumId`)
    REFERENCES `chinook`.`album` (`AlbumId`),
  CONSTRAINT `FK_TrackGenreId`
    FOREIGN KEY (`GenreId`)
    REFERENCES `chinook`.`genre` (`GenreId`),
  CONSTRAINT `FK_TrackMediaTypeId`
    FOREIGN KEY (`MediaTypeId`)
    REFERENCES `chinook`.`mediatype` (`MediaTypeId`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `chinook`.`invoiceline`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `chinook`.`invoiceline` (
  `InvoiceLineId` INT NOT NULL,
  `InvoiceId` INT NOT NULL,
  `TrackId` INT NOT NULL,
  `UnitPrice` DECIMAL(10,2) NOT NULL,
  `Quantity` INT NOT NULL,
  PRIMARY KEY (`InvoiceLineId`),
  INDEX `IFK_InvoiceLineInvoiceId` (`InvoiceId` ASC) VISIBLE,
  INDEX `IFK_InvoiceLineTrackId` (`TrackId` ASC) VISIBLE,
  CONSTRAINT `FK_InvoiceLineInvoiceId`
    FOREIGN KEY (`InvoiceId`)
    REFERENCES `chinook`.`invoice` (`InvoiceId`),
  CONSTRAINT `FK_InvoiceLineTrackId`
    FOREIGN KEY (`TrackId`)
    REFERENCES `chinook`.`track` (`TrackId`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `chinook`.`playlist`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `chinook`.`playlist` (
  `PlaylistId` INT NOT NULL,
  `Name` VARCHAR(120) CHARACTER SET 'utf8mb3' NULL DEFAULT NULL,
  PRIMARY KEY (`PlaylistId`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `chinook`.`playlisttrack`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `chinook`.`playlisttrack` (
  `PlaylistId` INT NOT NULL,
  `TrackId` INT NOT NULL,
  PRIMARY KEY (`PlaylistId`, `TrackId`),
  INDEX `IFK_PlaylistTrackPlaylistId` (`PlaylistId` ASC) VISIBLE,
  INDEX `IFK_PlaylistTrackTrackId` (`TrackId` ASC) VISIBLE,
  CONSTRAINT `FK_PlaylistTrackPlaylistId`
    FOREIGN KEY (`PlaylistId`)
    REFERENCES `chinook`.`playlist` (`PlaylistId`),
  CONSTRAINT `FK_PlaylistTrackTrackId`
    FOREIGN KEY (`TrackId`)
    REFERENCES `chinook`.`track` (`TrackId`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

"""

# Questions in natural language

question_1 = """Who are the 10 customers who spent the most in the store, 
    showing their full name, country, and total amount spent, ordered from 
    highest to lowest spending? If necessary, use the appropriate SQL window 
    function, as well as the WITH clause for the main query."""

# Foi necessário alterar o prompt
question_2 = """For each month of 2021, display the total accumulated sales up to 
    that month (cumulative sum) in 'YYYY-MM' format and the accumulated amount in dollars. 
    If necessary, use the appropriate SQL window function, as well as the WITH clause for the main query."""    

question_2 = """For each month of 2021 in 'YYYY-MM' format display the total sales up to that month,
    as well as the cumulative total of sales up to the current month, adding the value of the current 
    month with the previous ones. If necessary, use the appropriate SQL window function, as well as the 
    WITH clause for the main query."""    

question_3 = """For a specific customer (e.g. CustomerId = 42), list the invoices 
    sorted by date and show for each invoice: the date, the amount and the difference 
    in dollars to the previous invoice. If necessary, use the appropriate SQL window 
    function, as well as the WITH clause for the main query."""    

question_4 = """For each genre, display the 3 most popular tracks (in number of sales), 
    showing the track name, genre name and how many times this track has been sold. 
    Order by genre. If necessary, use the appropriate SQL window function, as well as the 
    WITH clause for the main query."""    

question_5 = """List all the tracks (TrackId and Name) together with the quantity sold 
    in the last invoice recorded and compare it with the quantity sold in the previous 
    invoice (to measure the variation), considering the invoices sorted by global date.
    If necessary, use the appropriate SQL window function, as well as the 
    WITH clause for the main query."""    

# A consulta do documento difere quanto ao resultado
question_6 = """For each customer, calculate the average time (in days) between the last 
    two invoices issued. Display CustomerId, full name and this average (only customers with 
    at least two invoices). If necessary, use the appropriate SQL window function, as well as the 
    WITH clause for the main query."""   

# A consulta do documento difere quanto ao resultado
question_7 = """List customers who have made more than one purchase, displaying their full 
    name, date of first and last purchase, and the number of days between purchases. Sort by 
    descending interval. If necessary, use the appropriate SQL window function, as well as the 
    WITH clause for the main query."""    

# A consulta do documento difere quanto ao resultado
question_8 = """Each invoice has a SupportRepId (employee). Sort employees by total revenue 
    generated (sum of all invoices for which they were support reps), showing EmployeeId, 
    full name, title and total revenue, in descending order. If necessary, use the appropriate 
    SQL window function, as well as the WITH clause for the main query."""    

# A consulta do documento difere quanto ao resultado
question_9 = """Calculate the weekly revenue moving average for the entire set of 2021 
    (start), total revenue for the week and the moving average of revenue. If necessary, 
    use the appropriate SQL window function, as well as the WITH clause for the main query."""    

# Erro. Não inclui a tabela playlist, somente a playlisttrack
question_10 = """Find playlists containing more than 50 tracks and, for each one, 
    determine the most frequent genre in the tracks. Display the playlist id, playlist name 
    and predominant genre. If necessary, use the appropriate SQL window function, as well as 
    the WITH clause for the main query."""    

question = question_10

# Instancia a pipeline e executa
pipeline = TextToSQLPipeline()
result_df = pipeline.run(question, schema_description)

# Mostra os resultados
print("\nResultado da consulta:")
print(result_df)