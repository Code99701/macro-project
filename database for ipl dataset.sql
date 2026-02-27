-- CREATE DATABASE ipl_database;
USE ipl_database;

-- CREATE TABLE Teams (
--     team_id INT PRIMARY KEY AUTO_INCREMENT,
--     team_name VARCHAR(100) UNIQUE
-- );

-- CREATE TABLE Venues (
--     venue_id INT PRIMARY KEY AUTO_INCREMENT,
--     venue_name VARCHAR(150) UNIQUE,
--     city VARCHAR(100)
-- );

-- CREATE TABLE Players (
--     player_id INT PRIMARY KEY AUTO_INCREMENT,
--     player_name VARCHAR(100) UNIQUE
-- );

-- CREATE TABLE Matches (
--     match_id INT PRIMARY KEY,
--     match_date DATE,
--     venue_id INT,
--     team1_id INT,
--     team2_id INT,
--     toss_winner_id INT,
--     winner_id INT,
--     result VARCHAR(50),
--     result_margin INT,

--     FOREIGN KEY (venue_id) REFERENCES Venues(venue_id),
--     FOREIGN KEY (team1_id) REFERENCES Teams(team_id),
--     FOREIGN KEY (team2_id) REFERENCES Teams(team_id),
--     FOREIGN KEY (toss_winner_id) REFERENCES Teams(team_id),
--     FOREIGN KEY (winner_id) REFERENCES Teams(team_id)
-- );

-- SHOW TABLES;

-- INSERT INTO Teams (team_name)
-- SELECT DISTINCT team1 FROM processed_matches
-- UNION
-- SELECT DISTINCT team2 FROM processed_matches;

-- INSERT INTO Venues (venue_name, city)
-- SELECT venue, MIN(city)
-- FROM processed_matches
-- GROUP BY venue;

-- INSERT INTO Players (player_name)
-- SELECT DISTINCT player_of_match FROM processed_matches;

-- SELECT * FROM Teams;
-- SELECT * FROM Venues;
-- SELECT * FROM Players;

-- INSERT INTO Players (player_name)
-- SELECT DISTINCT player_of_match
-- FROM processed_matches;

-- INSERT INTO Matches (
--     match_id,
--     match_date,
--     venue_id,
--     team1_id,
--     team2_id,
--     toss_winner_id,
--     winner_id,
--     result,
--     result_margin
-- )
-- SELECT
--     pm.id,
--     pm.date,

--     v.venue_id,

--     t1.team_id,
--     t2.team_id,

--     tw.team_id,
--     w.team_id,

--     pm.result,
--     pm.result_margin

-- FROM processed_matches pm

-- JOIN Venues v ON pm.venue = v.venue_name
-- JOIN Teams t1 ON pm.team1 = t1.team_name
-- JOIN Teams t2 ON pm.team2 = t2.team_name
-- JOIN Teams tw ON pm.toss_winner = tw.team_name
-- LEFT JOIN Teams w ON pm.winner = w.team_name;

-- SELECT * FROM Matches;

-- SELECT COUNT(*) FROM Matches;

-- SELECT 
--     m.match_id,
--     t1.team_name AS team1,
--     t2.team_name AS team2,
--     w.team_name AS winner,
--     v.venue_name
-- FROM Matches m

-- JOIN Teams t1 ON m.team1_id = t1.team_id
-- JOIN Teams t2 ON m.team2_id = t2.team_id
-- LEFT JOIN Teams w ON m.winner_id = w.team_id
-- JOIN Venues v ON m.venue_id = v.venue_id;

SELECT 
    t.team_name,
    COUNT(*) AS total_wins
FROM Matches m
JOIN Teams t ON m.winner_id = t.team_id
GROUP BY t.team_name
ORDER BY total_wins DESC;
