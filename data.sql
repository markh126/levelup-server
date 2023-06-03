SELECT * 
FROM levelupapi_eventgamer;

SELECT
    g.title,
    COUNT(e.id) event_count
FROM levelupapi_game g
    JOIN levelupapi_event e ON e.game_id = g.id
GROUP BY g.title