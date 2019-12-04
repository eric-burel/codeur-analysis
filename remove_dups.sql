/* We need a temporary table */
DROP TABLE  IF EXISTS tmp_scraper_codeurproject;
CREATE TABLE tmp_scraper_codeurproject as 
(
    SELECT * from (SELECT DISTINCT * FROM scraper_codeurproject) as d
);
DELETE from scraper_codeurproject;
INSERT INTO scraper_codeurproject 
SELECT * from tmp_scraper_codeurproject;
DROP TABLE tmp_scraper_codeurproject;