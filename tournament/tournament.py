#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    delete_matches_query = "DROP TABLE IF EXISTS matches;"
    connection = connect()  
    cursor = connection.cursor()
    cursor.execute(delete_matches_query)
    connection.commit()
    connection.close()

def deletePlayers():
    """Remove all the player records from the database."""
    delete_players_query = "DROP TABLE IF EXISTS players;"
    connection = connect()
    cursor = connection.cursor()
    cursor.execute(delete_players_query)
    connection.commit()
    connection.close()

def countPlayers():
    """Returns the number of players currently registered."""
    query = "SELECT COUNT(name) as num FROM players;"
    connection = connect()
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()[0]
    connection.commit()
    connection.close()



def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    query = "INSERT INTO players VALUES(%s);"
    connection = connect()
    cursor = connection.cursor()
    cursor.execute(query, (name,))
    connection.commit()
    connection.close()

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    query = "SELECT * FROM players ORDER BY wins DESC;"
    connection = connect()
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    connection.close()
    return result

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    match_query = "INSERT INTO matches VALUES(winner_id, loser_id) (%s, %s);"
    win_query = "UPDATE players SET num_match = num_match+1, wins = wins+1 where player_id = %s;"
    lose_query = "UPDATE players SET num_match = num_match+1 where player_id = %s;"
    connection = connect()
    cursor = connection.cursor()
    cursor.execute(match_query, (winner,), (loser,) )
    cursor.execute(win_query, (winner,))
    cursor.execute(lose_query, (loser,))
    connection.commit()
    connection.close()
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    pair = ()
    playerList = playerStandings()
    for i in range (0, len(playerList), 2):
        p1 = playerList[i][0] + playerList[i][1]
        p2 = playerList[i+1][0] + playerList[i+1][1]
        pair = pair + p1 + p2
    return pair

