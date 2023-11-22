from flask import Flask, jsonify, request
import ipl

app = Flask(__name__)


@app.route('/')
def get_intro_page():
    text = """Introduction Page made by Ishwar Gupta"""

    l = ["/api/team-names", "/api/teamvteam?team1='<team1name>'&team2=<team2name>",
         "/api/team-record?team=<any_team_name>"]
    api = {}
    for i in range(len(l)):
        api[i] = l[i]

    response = ipl.teams_name()

    return jsonify({"Home Page": text, "My APIs": api, "_All Teams Name": response})


@app.route('/api/team-names')
def team_name():
    response = ipl.teams_name()
    return response


@app.route('/api/teamvteam')
def team_v_team():
    team1 = request.args.get('team1')
    team2 = request.args.get('team2')
    response = ipl.teamvteam(team1, team2)
    return jsonify(response)


@app.route('/api/team-record')
def team_record():
    team = request.args.get('team')
    response = ipl.team_record(team)
    return response


@app.route('/api/batsman-names')
def batter_names():
    response = ipl.batsman_names()
    return response


@app.route('/api/batsman-record')
def batter_record():
    batsman = request.args.get('batsman')
    response = ipl.batsman_record(batsman)
    return response


app.run(debug=True)
