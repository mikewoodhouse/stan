WITH pt AS (
    SELECT *
    , ROW_NUMBER() OVER (PARTITION BY year, wicket ORDER BY total DESC) AS rank
    FROM partnerships
    WHERE year = ':year'
)
SELECT pt.*
, b1.surname || CASE WHEN b1.initial BETWEEN 'A' AND 'Z' THEN ', ' || b1.initial ELSE '' END AS bat1_name
, b2.surname || CASE WHEN b2.initial BETWEEN 'A' AND 'Z' THEN ', ' || b2.initial ELSE '' END AS bat2_name
FROM pt
JOIN players b1 ON b1.id = pt.bat1_id
JOIN players b2 ON b2.id = pt.bat2_id
WHERE total >= ':min_total'
OR rank = 1
ORDER BY wicket, total DESC