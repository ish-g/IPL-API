import pandas as pd
import numpy as np
import json

df = pd.read_csv(
    'https://docs.google.com/spreadsheets/d/e/2PACX-1vQNMuywEZLrkFw8wmNL38_hRdsMbsFF83A_w_kXwOvrDoNJ-S2ATdPld8tg41F4vSZs4I7dv3YUZNW8/pub?gid=986987377&single=true&output=csv')
df1 = pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vS7-ExDX7zYC5CxfFplHAwTSQUdGCgAfFDhLyBuz3OPxGacrdzhgfhOKPbLb2WwIf-YV8xUP66EB03B/pub?gid=1991064989&single=true&output=csv')

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)


def teams_name():
    names = pd.concat((df['Team1'], df['Team2'])).unique().tolist()
    dict1 = {}
    for i, team in enumerate(names):
        dict1[i] = team
    team_dict = {
        'team_names': dict1
    }
    return team_dict


def batsman_names():
    l6 = df1.groupby('batter')['ballnumber'].count().sort_values(ascending=False).head(80).index.tolist()
    dict7 = {"Batsman Names": l6}
    return json.dumps(dict7, cls=NpEncoder)


def batsman_record(batsman):
    four_df = df1[(df1['batter'] == batsman) & (df1['batsman_run'] == 4)]
    six_df = df1[(df1['batter'] == batsman) & (df1['batsman_run'] == 6)]
    four_count = four_df.groupby('ballnumber')['total_run'].count()
    six_count = six_df.groupby('ballnumber')['total_run'].count()
    total_four = four_count.sum()
    total_six = six_count.sum()
    four_counts = round(four_count / total_four * 100).values.tolist()
    six_counts = round(six_count / total_six * 100).values.tolist()
    dict11 = {"Total Four": four_counts, "Total Six": six_counts}
    dict12 = {"Batsman Record": dict11}
    return json.dumps(dict12, cls=NpEncoder)


def teamvteam(team1, team2):
    valid_teams = pd.concat((df['Team1'], df['Team2'])).unique().tolist()
    if team1 in valid_teams and team2 in valid_teams:
        temp_df = df[(df['Team1'] == team1) & (df['Team2'] == team2) | (df['Team1'] == team2) & (df['Team2'] == team1)]
        total_matches = temp_df.shape[0]
        w1 = temp_df['WinningTeam'].value_counts()[team1]
        w2 = temp_df['WinningTeam'].value_counts()[team2]

        dict1 = {

            'Total_matches': str(total_matches),
            team1: str(w1),
            team2: str(w2),
            'Draw': str(total_matches - (w1 + w2))
        }
        dict1 = {'teamvteam': dict1}
        return dict1
    else:
        return {'message': 'Check Spelling'}


def team_record(team):

    temp_df = df[(df['Team1'] == team) | (df['Team2'] == team)]
    total_match_played = temp_df.shape[0]
    won = temp_df['WinningTeam'].value_counts()[team]
    loss = temp_df['WinningTeam'].value_counts().sum() - won
    no_result = total_match_played - (won + loss)
    dict1 = {
        'MatchesPlayed': total_match_played,
        'Won': won,
        'Loss': loss,
        'NoResult': no_result
    }

    team_names = pd.concat((df['Team1'], df['Team2'])).unique().tolist()
    team_names.remove(team)
    dict2 = {}
    for i in team_names:
        temp_df1 = temp_df[(temp_df['Team1'] == i) | (temp_df['Team2'] == i)]
        matches_played = temp_df1.shape[0]
        try:
            won1 = temp_df1['WinningTeam'].value_counts()[team]
        except:
            won1 = 0
        if i in temp_df1['WinningTeam'].value_counts():
            loss1 = temp_df1['WinningTeam'].value_counts()[i]
        else:
            loss1 = 0
        no_result1 = matches_played - (won1 + loss1)
        dict2[i] = {
            'MatchesPlayed': matches_played,
            'Won': won1,
            'Loss1': loss1,
            'NoResult': no_result1
        }
    dict3 = {'Team-Record': {'Overall': dict1, 'Against': dict2}}
    return json.dumps(dict3, cls=NpEncoder)

