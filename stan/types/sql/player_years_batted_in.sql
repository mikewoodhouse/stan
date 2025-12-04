SELECT DISTINCT
    strftime ('%Y', datetime (match_date)) AS yr
FROM
    match_batting
WHERE
    player_id = ':player_id'
ORDER BY
    1