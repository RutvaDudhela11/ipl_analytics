-- ============================================================
--  IPL Cricket Analytics — SQL Queries
--  Database  : SQLite / PostgreSQL / MySQL (syntax compatible)
--  Tables    : matches, deliveries
-- ============================================================

-- ── TABLE SCHEMAS (for reference) ───────────────────────────
-- matches    (id, season, team1, team2, toss_winner, toss_decision, winner, player_of_match, venue, city)
-- deliveries (match_id, inning, over, ball, batter, bowler, batsman_runs, extra_runs, total_runs, dismissal_kind, player_dismissed)


-- ─────────────────────────────────────────────────────────────
-- Q1. Total wins per team (all time)
-- ─────────────────────────────────────────────────────────────
SELECT
    winner                          AS team,
    COUNT(*)                        AS total_wins
FROM matches
WHERE winner IS NOT NULL
GROUP BY winner
ORDER BY total_wins DESC
LIMIT 10;


-- ─────────────────────────────────────────────────────────────
-- Q2. Season-wise champion (most wins per season)
-- ─────────────────────────────────────────────────────────────
WITH season_wins AS (
    SELECT
        season,
        winner              AS team,
        COUNT(*)            AS wins,
        RANK() OVER (PARTITION BY season ORDER BY COUNT(*) DESC) AS rk
    FROM matches
    WHERE winner IS NOT NULL
    GROUP BY season, winner
)
SELECT season, team, wins
FROM season_wins
WHERE rk = 1
ORDER BY season;


-- ─────────────────────────────────────────────────────────────
-- Q3. Top 10 run-scorers of all time
-- ─────────────────────────────────────────────────────────────
SELECT
    batter,
    SUM(batsman_runs)       AS total_runs,
    COUNT(*)                AS balls_faced,
    ROUND(
        SUM(batsman_runs) * 100.0 / NULLIF(COUNT(*), 0), 2
    )                       AS strike_rate
FROM deliveries
GROUP BY batter
ORDER BY total_runs DESC
LIMIT 10;


-- ─────────────────────────────────────────────────────────────
-- Q4. Top 10 wicket-takers (excluding run-outs & retired hurt)
-- ─────────────────────────────────────────────────────────────
SELECT
    bowler,
    COUNT(*)                AS wickets
FROM deliveries
WHERE
    dismissal_kind IS NOT NULL
    AND dismissal_kind NOT IN ('run out', 'retired hurt', 'obstructing the field')
GROUP BY bowler
ORDER BY wickets DESC
LIMIT 10;


-- ─────────────────────────────────────────────────────────────
-- Q5. Economy rate of bowlers (min 50 overs bowled)
-- ─────────────────────────────────────────────────────────────
SELECT
    bowler,
    SUM(total_runs)                                         AS runs_conceded,
    COUNT(*) / 6                                            AS overs_bowled,
    ROUND(SUM(total_runs) * 6.0 / NULLIF(COUNT(*), 0), 2)  AS economy_rate
FROM deliveries
GROUP BY bowler
HAVING COUNT(*) / 6 >= 50
ORDER BY economy_rate ASC
LIMIT 10;


-- ─────────────────────────────────────────────────────────────
-- Q6. Toss decision win rate
-- ─────────────────────────────────────────────────────────────
SELECT
    toss_decision,
    COUNT(*)                                                AS total_matches,
    SUM(CASE WHEN toss_winner = winner THEN 1 ELSE 0 END)  AS toss_winner_won,
    ROUND(
        SUM(CASE WHEN toss_winner = winner THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1
    )                                                       AS win_pct
FROM matches
WHERE winner IS NOT NULL
GROUP BY toss_decision;


-- ─────────────────────────────────────────────────────────────
-- Q7. Player of the match leaderboard
-- ─────────────────────────────────────────────────────────────
SELECT
    player_of_match,
    COUNT(*)            AS awards
FROM matches
WHERE player_of_match IS NOT NULL
GROUP BY player_of_match
ORDER BY awards DESC
LIMIT 10;


-- ─────────────────────────────────────────────────────────────
-- Q8. Highest-scoring over in IPL history
-- ─────────────────────────────────────────────────────────────
SELECT
    match_id,
    inning,
    over,
    SUM(total_runs)     AS runs_in_over
FROM deliveries
GROUP BY match_id, inning, over
ORDER BY runs_in_over DESC
LIMIT 10;


-- ─────────────────────────────────────────────────────────────
-- Q9. Season-wise total runs scored
-- ─────────────────────────────────────────────────────────────
SELECT
    m.season,
    SUM(d.total_runs)   AS total_runs
FROM deliveries d
JOIN matches m ON d.match_id = m.id
GROUP BY m.season
ORDER BY m.season;


-- ─────────────────────────────────────────────────────────────
-- Q10. Head-to-head record between two teams
--       Change the team names as needed
-- ─────────────────────────────────────────────────────────────
SELECT
    winner,
    COUNT(*)            AS wins
FROM matches
WHERE
    (team1 = 'Mumbai Indians' AND team2 = 'Chennai Super Kings')
    OR
    (team1 = 'Chennai Super Kings' AND team2 = 'Mumbai Indians')
GROUP BY winner;
