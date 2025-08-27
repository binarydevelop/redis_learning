from redis_connection import redis_client
from helpers import generate_random_string_with_repetition
from random import randint, choice
import time 

# Add multiple players in the leader board intially with 0 score 
def add_players(count = 1, default_Score = 0):
    players = {}
    for i in range(count):
        player_name = generate_random_string_with_repetition(6)
        players[player_name] = default_Score
        
    redis_client.zadd("leaderboard", players)
    return list(players.keys())
        

# Increase random player scores very rapidly 
def increase_scores_for_random_players(records_to_update = 10, score_to_increase = randint(1, 50)):
    players = redis_client.zrange("leaderboard", 0, -1)

    for _ in range(records_to_update):
        player = choice(players)
        point = randint(1, score_to_increase)
        
        redis_client.zincrby("leaderboard", point, player)
        return None
        
# Get the real time lreaderboard 
def get_leaderboard(retrieve_top = 10):
    players = redis_client.zrevrange("leaderboard", 0, retrieve_top-1, withscores= True)
    for player, score in players:
        print(player, score)
        
    return None
    
# Feature to get any players score at any time 
def retrieve_player_details(name):
    player_details = redis_client.zscore("leaderboard", name)
    print(player_details)
    return player_details

#demo
add_players(100)
for _ in range(10):
    print(time.time())
    increase_scores_for_random_players(100)
    time.sleep(3)
    print('-------------------LeaderBoard -----------------', time.strftime("%H:%M:%S"))
    get_leaderboard()
    