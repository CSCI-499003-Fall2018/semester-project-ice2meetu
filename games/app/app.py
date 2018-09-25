from flask import Flask, request, jsonify, session
import random
import os
import pickle
import pandas as pd

app = Flask(__name__)

#will be later moved to database
games_df = pd.read_pickle('games.pickle')

@app.route('/')
def any_game():
    game_index = random.choice(list(games_df.index))
    return jsonify({'index': int(game_index),
                    'game': games_df.at[game_index,'game'],
                    'text': games_df.at[game_index,'text']})

@app.route('/<int:num_players>')
def get_game(num_players):
    games_sample = set()
    for index, row in games_df.iterrows():
        game_nplayers = row['num_players']
        if num_players in game_nplayers:
            games_sample.add(index)

    game_index = random.choice(list(games_sample))

    return jsonify({'index': int(game_index),
                    'game': games_df.at[game_index,'game'],
                    'text': games_df.at[game_index,'text']})

if __name__ == '__main__':
    app.run()
