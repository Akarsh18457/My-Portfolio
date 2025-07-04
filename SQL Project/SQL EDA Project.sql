SELECT *
FROM layoffs_staging2;


SELECT MAX(total_laid_off)
FROM layoffs_staging2;

-- Looking at Percentage to see how big these layoffs were
SELECT MAX(percentage_laid_off), MIN(percentage_laid_off)
FROM layoffs_staging2
WHERE percentage_laid_off IS NOT NULL;


SELECT *
FROM layoffs_staging2
WHERE percentage_laid_off = 1;
-- these are mostly startups it looks like who all went out of business during this time

SELECT *
FROM layoffs_staging2
WHERE percentage_laid_off = 1
ORDER BY funds_raised_millions DESC;
-- Britishvolt is a transportation company and Quibi which is a media comapny raised around 2 billion dollars and went under!



-- Companies with the biggest single Layoff

SELECT company, total_laid_off
FROM layoffs_staging2
ORDER BY 2 DESC;

-- now that's just on a single day

-- Companies with the most Total Layoffs
SELECT company, SUM(total_laid_off)
FROM layoffs_staging2
GROUP BY company
ORDER BY 2 DESC
LIMIT 10;

-- by location
SELECT location, SUM(total_laid_off)
FROM layoffs_staging2
GROUP BY location
ORDER BY 2 DESC
LIMIT 10;


SELECT MIN(`date`) ,MAX(`date`)
FROM layoffs_staging2;

-- this it total in the past 3 years or in the dataset

SELECT country, SUM(total_laid_off)
FROM layoffs_staging2
GROUP BY country
ORDER BY 2 DESC;
-- U.S(approx. 500k) and India(approx. 70k) had the most layoffs.

SELECT YEAR(`date`), SUM(total_laid_off)
FROM layoffs_staging2
GROUP BY YEAR(`date`)
ORDER BY 1 ASC;
-- in year 2022 most layoffs took place i.e. around 300k

SELECT industry, SUM(total_laid_off)
FROM layoffs_staging2
GROUP BY industry
ORDER BY 2 DESC;
-- the consumer industry faced most layoffs i.e. approx. 94k 

SELECT stage, SUM(total_laid_off)
FROM layoffs_staging2
GROUP BY stage
ORDER BY 2 DESC;
-- and the Post-IPO companies gave the most layoffs approx. 400k .


-- Earlier we looked at Companies with the most Layoffs. Now let's look at that per year.
WITH Company_Year AS
(
	SELECT company, YEAR(`date`) AS years, SUM(total_laid_off) AS total_laid_off
    FROM layoffs_staging2
    GROUP BY company, YEAR(`date`)
),
 Company_Year_Rank AS (
  SELECT company, years, total_laid_off ,
  DENSE_RANK() OVER (PARTITION BY years ORDER BY total_laid_off DESC )AS ranking
  FROM Company_Year
  )
SELECT company, years, total_laid_off , ranking 
FROM Company_Year_Rank
WHERE ranking <=3
AND years IS NOT NULL
ORDER BY years ASC, total_laid_off DESC;


-- Rolling Total of Layoffs Per Month
SELECT SUBSTRING(`date`,1,7) AS dates, SUM(total_laid_off) AS total_laid_off
FROM layoffs_staging2
GROUP BY dates
ORDER BY dates ASC;

WITH DATE_CTE AS
(
SELECT SUBSTRING(`date`,1,7) AS dates, SUM(total_laid_off) AS total_laid_off
FROM layoffs_staging2
GROUP BY dates
ORDER BY dates ASC
)
SELECT dates, total_laid_off, SUM(total_laid_off) OVER (ORDER BY dates ASC) AS rolling_total_layoffs
FROM DATE_CTE
ORDER BY dates ASC;


-- it is concluded that 2022 wa the worst year for some of the biggest companies.

