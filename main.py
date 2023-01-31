from flask import Flask, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from forms import CreateMatchForm
from flask_gravatar import Gravatar
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from functools import wraps
from flask import abort
import os
import pandas as pd
from IPython.display import HTML
import plotly.express as px
import plotly.io as pio
from plotly.offline import plot
from plotly.graph_objs import Scatter
from flask import Markup
pio.templates.default = "plotly_white"

data = pd.read_csv("t20 world cup 22.csv")


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
df = pd.read_csv("t20-world-cup-22.csv", index_col=False)
arr = []
links = ['https://2022.t20worldcup.com/video/2853918']
for index, row in df.iterrows():
    winner = row["winner"]
    if row["won by"] == "Runs":
        runs = int(row["first innings score"] - row["second innings score"])

        arr.append(f"{winner} won by {runs} runs")
    elif row["won by"] == "Wickets":
        wickets_left = int(10 - row["second innings wickets"])

        arr.append(f"{winner} won by {wickets_left} wickets")
    else:
        arr.append("No Result")
df["Result"] = arr
@app.route('/signup',methods=['POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        new_user = User(
            name=name,
            email=email,
            password=password
        )
        db.session.add(new_user)
        db.session.commit()
        return "User signed up successfully"


@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user is not None and user.check_password(password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')

@app.route('/schedule')
def schedule():
    new_df = df[["venue", "stage", "team1", "team2", "Result"]]
    pd.set_option('colheader_justify', 'center')  # FOR TABLE <th>

    html_string = '''
    <html>
      <head>
      <title>ICC t20 World Cup Schedule</title>
      <style> 
         bal
         {{
            width: 100%;
         }}
         table.a
          {{
            border-collapse: collapse;
            margin: 25px 0;
            font-size: 3rem;
            font-family: sans-serif;
            width: 100%;
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);
            }}
         table
          {{
            border-collapse: collapse;
            margin: 25px 0;
            font-size: 3rem;
            font-family: sans-serif;
            width: 100%;
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);
            }}
        tr {{
        
        background-color: #009879;;
        color: #ffffff;
        text-align: left;
        }}
        th {{
        background-color: green;;
        color: #ffffff;
        padding: 12px 15px;
        }}
        td {{
        padding: 12px 15px;
        }}
      </style>
      </head>
      <body>
        
        <div class="bal"> 
        <table class="a">
        <tr>
        <td>
        <img src="static/img/t20_logo.jpg" width=90%>
        </td>
        <td>
        <h1 align="center">Fixtures of T20 World Cup 2022</h1>
        </td>
        </table>
        </div>
        {table}
      </body>
    </html>.
    '''

    # OUTPUT AN HTML FILE
    with open('templates/schedule.html', 'w') as f:
        f.write(html_string.format(table=new_df.to_html()))

    return render_template("schedule.html")


@app.route('/get_details')
def get_details_about_match():
    # form = CreateMatchForm()
    # if form.validate_on_submit():
    first_team = "India"
    second_team = "England"
    # Check if user's email address already exists
    # if User.query.filter_by(email=form.email.data).first:
    #     # Send flash message
    #     flash("You've already signed up with that email, log in instead!")
    #     # Redirect to /login route.
    #     return redirect(url_for('login'))
    # hash_and_salted_password = generate_password_hash(
    #     form.password.data,
    #     method='pbkdf2:sha256',
    #     salt_length=8
    # )
    # new_user = User(
    #     email=form.email.data,
    #     name=form.name.data,
    #     password=hash_and_salted_password
    # )
    #
    # db.session.add(new_user)
    # db.session.commit()
    #
    # # This line will authenticate the users with Flask login
    # login_user(new_user)
    # return redirect(url_for("get_all_posts"))

    result = df.query(
        "(team1 == @first_team and team2 == @second_team) or team1 == @second_team and team2 == @first_team")
    seriees = list(result["Result"])
    team1 = list(result.get('team1'))[0]
    team2 = list(result.get('team2'))[0]
    stage = list
    if seriees[0] != "No Result" and list(result.get('stage'))[0] != 'Final':

        venue = list(result.get('venue'))[0]
        toss_won = list(result.get('toss winner'))[0]
        decision = list(result.get('toss decision'))[0]
        team_won = list(result.get('winner'))[0]
        answer = f"{seriees[0]} . The match took place in {venue} . {toss_won} won the toss and chose to {decision} first." \
                 "It was a great performance from both sides but the winning team could adjust to the conditions " \
                 "better and " \
                 "emerged " \
                 "victorious at the end. "

        return render_template(f"{team1}vs{team2}.html", answer=answer, link=link)
    elif seriees[0] != "No Result":
        return redirect(url_for('final'))


@app.route('/final')
def final():
    result = df.query("stage == 'Final'")
    seriees = list(result["Result"])
    venue = list(result.get('venue'))[0]
    toss_won = list(result.get('toss winner'))[0]
    decision = list(result.get('toss decision'))[0]
    team_won = list(result.get('winner'))[0]
    most_score = list(result.get('highest score'))[0]
    top_score = list(result.get('top scorer'))[0]
    best_bowler = list(result.get('best bowler'))[0]
    bowling_figure = list(result.get('best bowling figure'))[0]
    player_of_the_match = list(result.get('player of the match'))[0]
    if team_won == toss_won:

        answer = f"The final match took place in {venue} . {toss_won} won the toss and chose to {decision} first ." \
                 f"The decision to {decision} proved very beneficial and took a major role in the game. " \
                 f"{seriees[0]}. {top_score} scored {most_score} with brilliant timming and proved costly to the bowler. " \
                 "It was a great performance from both sides but the winning team could adjust to the conditions " \
                 "better and " \
                 "emerged " \
                 "victorious at the end ."
    else:

        answer = f"The final match took place in {venue} . {toss_won} won the toss and chose to {decision} first ." \
                 f"The decision to {decision} proved hard to the losing team and played a important part in the match. " \
                 f"{seriees[0]}. {top_score} scored {most_score} with brilliant timming and proved costly to the bowler. " \
                 "It was a great performance from both sides but the winning team could adjust to the conditions " \
                 "better and " \
                 "emerged " \
                 "victorious at the end ."
    return render_template("winner.html", answer=answer, link=link)


@app.route('/semi_finale')
def semi_finale():
    def make_clickable(url, name):
        return '<a href="{}" rel="noopener noreferrer" target="_blank">{}</a>'.format(url, name)

    result = df.query("stage == 'Semi-final'")
    link1 = render_template("semi-final1.html", links_semf[0])
    link2 = render_template("semi-final2.html", links_semf[1])
    links_semf = [links[-3], links[-2]]
    result["links"] = links_semf
    new_df = result[["venue", "stage", "team1", "team2", "Result", "links"]]
    semi_finale_matches = []
    count = 0
    for index, value in result.iterrows():
        teama = result["team1"]
        teamb = result["team2"]
        semi_finale_matches.append("teama vs teamb")
        link = render_template(f"{teama}vs{teamb}.html", link=link[count])
        count += 1

    new_df["names"] = semi_finale_matches
    HTML(new_df.to_html(render_links=True, escape=False))

    new_df['highlights'] = new_df.apply(lambda x: make_clickable(x['links'], x['names']), axis=1)
    pd.set_option('colheader_justify', 'center')  # FOR TABLE <th>

    html_string = '''
        <html>
          <head>
          <title>Semi-Finals</title>
          <style> 
             bal
             {{
                width: 100%;
             }}
             table.a
              {{
                border-collapse: collapse;
                margin: 25px 0;
                font-size: 3rem;
                font-family: sans-serif;
                width: 100%;
                box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);
                }}
             table
              {{
                border-collapse: collapse;
                margin: 25px 0;
                font-size: 3rem;
                font-family: sans-serif;
                width: 100%;
                box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);
                }}
            tr {{

            background-color: #009879;;
            color: #ffffff;
            text-align: left;
            }}
            th {{
            background-color: green;;
            color: #ffffff;
            padding: 12px 15px;
            }}
            td {{
            padding: 12px 15px;
            }}
          </style>
          </head>
          <body>

            <div class="bal"> 
            <table class="a">
            <tr>
            <td>
            <img src="static/img/t20_logo.jpg" width=90%>
            </td>
            <td>
            <h1 align="center">Fixtures of Semi Finale T20 World Cup 2022</h1>
            </td>
            </table>
            </div>
            {table}
          </body>
        </html>.
        '''

    # OUTPUT AN HTML FILE
    with open('templates/semi-finale.html', 'w') as f:
        f.write(html_string.format(table=new_df.to_html()))

    return render_template("semi-finale.html", link=links_semf)

    # if seriees[0] != "No Result":
    #     venue = list(result.get('venue'))[0]
    #     toss_won = list(result.get('toss winner'))[0]
    #     decision = list(result.get('toss decision'))[0]
    #     team_won = list(result.get('winner'))[0]
    #     answer = f"{seriees[0]} . The match took place in {venue} . {toss_won} won the toss and chose to {decision} first." \
    #              "It was a great performance from both sides but the winning team could adjust to the conditions " \
    #              "better and " \
    #              "emerged " \
    #              "victorious at the end. "
    #
    #     return render_template("get_results.html", answer=answer, link=link)


@app.route("/get_best_player")
def get_tournament_best_player():
    # OUTPUT AN HTML FILE
    return render_template("best-player.html")


@app.route("/get_best_batsman")
def get_best_batsman():
    return render_template("best-batsman.html")


@app.route("/get_best_bowler")
def get_best_bowler():
    return render_template("best-bowler.html")


@app.route("/get_most_runs_by_a_batsman")
def get_most_scored_batsman():
    most_runs = 0

    for index, row in df.iterrows():
        if row["highest score"] and (row["highest score"]) > most_runs:
            most_runs = int(row["highest score"])
            batsman = row["top scorer"]


# @app.route("/get_best_wicket_stats")
def get_best_wicket_stats():
    max_wickets = 0
    calender = {"Jan":1,"Feb":2,"Mar":3,"Apr":4,"May":5,"Jun":6,"July":7,"Aug":8,"Sep":9,"Oct":10,"Nov":11,"Dec":12}
    for index, row in df.iterrows():

        try:

            wickets = int(row["best bowling figure"][0:2])
        except TypeError:
            wickets = wickets
        except:
            wickets = calender[row["best bowling figure"][0:3]]

        if wickets > max_wickets:
            max_wickets = wickets
            player = row["best bowler"]
def get_all_matches_played():
    team = request.args.get("team")
    result = df.query("team1 == @team or team2 == @team")
    result_df = result[["venue", "stage", "team1", "team2", "Result"]]
    # will be done after up is done
def about():

    figure = px.bar(data,
                    x=data["winner"],
                    title="Number of Matches Won by teams in t20 World Cup 2022")

    return render_template("best-player.html",)



# if __name__ == "__main__":
#     app.run(debug=True)
