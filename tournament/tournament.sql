-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP DATABASE IF EXISTS tournament;

CREATE DATABASE tournament;
\c tournament;

CREATE TABLE matches (
	match_id SERIAL PRIMARY KEY,
	winner_id integer,
	loser_id integer
);

CREATE TABLE players (
	player_id SERIAL PRIMARY KEY,
	name text,
	wins integer,
	num_match integer
);