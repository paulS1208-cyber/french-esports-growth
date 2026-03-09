import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# --- Lecture du CSV fusionné ---
df = pd.read_csv("merged_esports.csv", sep=";")

# Nettoyage de PrizeMoney
df["PrizeMoney"] = df["PrizeMoney"].astype(str).str.replace("[\$,]", "", regex=True)
df["PrizeMoney"] = pd.to_numeric(df["PrizeMoney"], errors='coerce').fillna(0)

# Création du dossier pour les graphiques
if not os.path.exists("graphs"):
    os.makedirs("graphs")

# Style seaborn
sns.set(style="whitegrid")
plt.rcParams['figure.figsize'] = (12,6)

# --- 1. Évolution des jeux actifs ---
plt.figure()
sns.lineplot(data=df, x="Year", y="GamesActive", hue="Team", marker="o")
plt.title("Évolution du nombre de jeux actifs par équipe")
plt.ylabel("Jeux actifs")
plt.xlabel("Année")
plt.xticks(sorted(df["Year"].unique()))
plt.legend(title="Équipe")
plt.savefig("graphs/games_active.png", dpi=300)
plt.close()

# --- 2. Évolution des tournois joués ---
plt.figure()
sns.lineplot(data=df, x="Year", y="TournamentsPlayed", hue="Team", marker="o")
plt.title("Évolution du nombre de tournois joués par équipe")
plt.ylabel("Tournois joués")
plt.xlabel("Année")
plt.xticks(sorted(df["Year"].unique()))
plt.legend(title="Équipe")
plt.savefig("graphs/tournaments_played.png", dpi=300)
plt.close()

# --- 3. Évolution des gains ---
plt.figure()
sns.lineplot(data=df, x="Year", y="PrizeMoney", hue="Team", marker="o")
plt.title("Évolution des gains par équipe")
plt.ylabel("PrizeMoney ($)")
plt.xlabel("Année")
plt.xticks(sorted(df["Year"].unique()))
plt.legend(title="Équipe")
plt.savefig("graphs/prizemoney.png", dpi=300)
plt.close()

# --- 4. Scatter : tournois joués vs gains ---
plt.figure()
sns.scatterplot(data=df, x="TournamentsPlayed", y="PrizeMoney", hue="Team", style="Team", s=100)
plt.title("Tournois joués vs PrizeMoney par équipe")
plt.xlabel("Tournois joués")
plt.ylabel("Gains ($)")
plt.legend(title="Équipe")
plt.savefig("graphs/scatter_tournaments_prizemoney.png", dpi=300)
plt.close()

# --- 5. Bar chart : gains totaux par équipe ---
plt.figure()
total_prize = df.groupby("Team")["PrizeMoney"].sum().sort_values(ascending=False).reset_index()
sns.barplot(data=total_prize, x="Team", y="PrizeMoney", palette="viridis")
plt.title("Gains totaux par équipe")
plt.ylabel("PrizeMoney ($)")
plt.xlabel("Équipe")
plt.xticks(rotation=45)
plt.savefig("graphs/total_prizemoney.png", dpi=300)
plt.close()

# --- 6. Heatmap : corrélation entre TournamentsPlayed, GamesActive, PrizeMoney ---
plt.figure()
corr_df = df.groupby(["Team","Year"])[["TournamentsPlayed","GamesActive","PrizeMoney"]].sum().corr()
sns.heatmap(corr_df, annot=True, fmt=".2f", cmap="coolwarm")
plt.title("Corrélation entre TournamentsPlayed, GamesActive et PrizeMoney")
plt.savefig("graphs/correlation_heatmap.png", dpi=300)
plt.close()

# --- 7. Stacked bar chart : Tournaments par année ---
stacked = df.pivot_table(index="Year", columns="Team", values="TournamentsPlayed", aggfunc="sum", fill_value=0)
stacked.plot(kind="bar", stacked=True)
plt.title("Nombre de tournois joués par année et par équipe")
plt.ylabel("Tournois joués")
plt.xlabel("Année")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("graphs/stacked_tournaments.png", dpi=300)
plt.close()

# --- 8. Cumulative PrizeMoney plot ---
cum_prize = df.groupby(["Team","Year"])["PrizeMoney"].sum().groupby(level=0).cumsum().reset_index()
plt.figure()
for team in cum_prize["Team"].unique():
    team_data = cum_prize[cum_prize["Team"] == team]
    plt.plot(team_data["Year"], team_data["PrizeMoney"], marker="o", label=team)
plt.title("Évolution cumulative des gains par équipe")
plt.ylabel("PrizeMoney cumulé ($)")
plt.xlabel("Année")
plt.xticks(sorted(df["Year"].unique()))
plt.legend(title="Équipe")
plt.savefig("graphs/cumulative_prizemoney.png", dpi=300)
plt.close()

# --- 9. Boxplot des gains par année ---
plt.figure()
sns.boxplot(data=df, x="Year", y="PrizeMoney")
plt.title("Distribution des gains par année")
plt.ylabel("PrizeMoney ($)")
plt.xlabel("Année")
plt.savefig("graphs/boxplot_prizemoney.png", dpi=300)
plt.close()

print("✅ Tous les graphiques ont été générés et sauvegardés dans le dossier 'graphs'.")