import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("t20-world-cup-22.csv")
score = 0
batsmen = {}
for index, row in df.iterrows():

    try:

        score = int(row["highest score"])

    except:
        score = 0
    batsman = row["top scorer"]

    if batsman not in batsmen and type(batsman) == str:
        batsmen[batsman] = score


    elif batsman in batsmen:
        batsmen[batsman] = max(score, batsmen[batsman])

print(batsmen)
