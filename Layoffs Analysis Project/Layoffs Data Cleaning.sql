SELECT * 
FROM layoffs;


-- creating a staging table. This is the one we will work in and clean the data. We want a table with the raw data in case something happens
CREATE TABLE world_layoffs.layoffs_staging
LIKE world_layoffs.layoffs;

SELECT * 
FROM layoffs_staging;

INSERT INTO layoffs_staging
SELECT * FROM world_layoffs.layoffs;



-- Removing Duplicates
SELECT * 
FROM layoffs_staging;

SELECT *
FROM (
		SELECT  company, location, industry, total_laid_off,percentage_laid_off,`date`, stage, country, funds_raised_millions,
				ROW_NUMBER() OVER(
						PARTITION BY company, location, industry, total_laid_off,percentage_laid_off,`date`, stage, country, funds_raised_millions
						) AS row_num
		FROM 
			layoffs_staging
) duplicates
WHERE 
		row_num>1;

SELECT * 
FROM layoffs_staging;


CREATE TABLE `layoffs_staging2` (
  `company` text,
  `location` text,
  `industry` text,
  `total_laid_off` int DEFAULT NULL,
  `percentage_laid_off` text,
  `date` text,
  `stage` text,
  `country` text,
  `funds_raised_millions` int DEFAULT NULL,
  row_num INT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


INSERT INTO `world_layoffs`.`layoffs_staging2`
(`company`,
`location`,
`industry`,
`total_laid_off`,
`percentage_laid_off`,
`date`,
`stage`,
`country`,
`funds_raised_millions`,
`row_num`)
SELECT  company,
 location, 
 industry, 
 total_laid_off,
 percentage_laid_off,
 `date`, 
 stage, 
 country, 
 funds_raised_millions,
				ROW_NUMBER() OVER(
						PARTITION BY company, location, industry, total_laid_off,percentage_laid_off,`date`, stage, country, funds_raised_millions
						) AS row_num
		FROM 
			layoffs_staging;


DELETE FROM layoffs_staging2
WHERE row_num>=2;

SELECT * 
FROM layoffs_staging2;


--  Standardizing Data
-- if we look at industry it looks like we have some null and empty rows, let's take a look at these
SELECT DISTINCT industry
FROM layoffs_staging2
ORDER BY industry;

SELECT *
FROM layoffs_staging2
WHERE industry IS NULL
OR industry = ''
ORDER BY industry;


SELECT *
FROM layoffs_staging2
WHERE company LIKE 'Bally%';
-- nothing wrong here

SELECT *
FROM layoffs_staging2
WHERE company LIKE 'airbnb%';
-- it looks like airbnb is a travel, but this one just isn't populated.

UPDATE layoffs_staging2
SET industry = null
WHERE industry = '';

SELECT * 
FROM layoffs_staging2
WHERE industry IS NULL
OR industry = ''
ORDER BY industry;

-- we need to populate those nulls if possible
UPDATE layoffs_staging2 t1
JOIN  layoffs_staging2 t2
ON 	t1.company = t2.company
SET t1.industry = t2.industry
WHERE t1.industry IS NULL
AND t2.industry IS NOT NULL;

SELECT *
FROM layoffs_staging2
ORDER BY industry;

-- it looks like Bally's was the only one without a populated row to populate this null values