DELETE FROM scraper_codeurproject
WHERE id IN (
    SELECT
        id
    FROM
        scraper_codeurproject
    GROUP BY
        id
    HAVING 
        COUNT(*) > 1
)