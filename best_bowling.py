import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
df = pd.read_csv("t20-world-cup-22.csv")

max_wickets = 0
calender = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6, "July": 7, "Aug": 8, "Sep": 9, "Oct": 10,
            "Nov": 11, "Dec": 12}
bowlers = {}
for index, row in df.iterrows():

    try:

        wickets = int(row["best bowling figure"][0:2])
    except TypeError:
        wickets = wickets
    except:
        wickets = calender[row["best bowling figure"][0:3]]
    player = row["best bowler"]
    if player not in bowlers and type(player) == str:
        bowlers[player] = wickets
    if wickets > max_wickets:

        max_wickets = wickets
        player = row["best bowler"]

        if player in bowlers:
            if bowlers[player] < max_wickets:
                bowlers[player] = max_wickets
# for value in bowlers:
name = list(bowlers.keys())
values = list(bowlers.values())
plt.figure(figsize=(8,4))
plt.xticks(
    rotation=45,
    horizontalalignment='right'
)
plt.bar(range(len(bowlers)), values, tick_label = name)

plt.show()