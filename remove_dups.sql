/* Solution with tmp table*/
/*
DROP TABLE  IF EXISTS tmp_scraper_codeurproject;
CREATE TABLE tmp_scraper_codeurproject as 
(
    SELECT * from (SELECT DISTINCT * FROM scraper_codeurproject) as d
);
DELETE from scraper_codeurproject;
INSERT INTO scraper_codeurproject 
SELECT * from tmp_scraper_codeurproject;
DROP TABLE tmp_scraper_codeurproject;
*/

/* solution using ctid (physical row position used as unique id) */
DELETE FROM scraper_codeurproject a USING (
      SELECT MIN(ctid) as ctid, id
        FROM scraper_codeurproject
        GROUP BY id HAVING COUNT(*) > 1
      ) b
      WHERE a.id = b.id
      AND a.ctid <> b.ctid
