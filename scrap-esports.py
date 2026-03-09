import pandas as pd
import re
import time

teams = ["Karmine_Corp", "Team_Vitality", "Solary", "Gentle_Mates"]
games = ["leagueoflegends", "rocketleague", "valorant", "trackmania", "counterstrike", "fortnite"]
all_data = []

def extract_year(date_str):
    try:
        return pd.to_datetime(date_str, errors="coerce").year
    except:
        match = re.search(r"(20\d{2})", str(date_str))
        if match:
            return int(match.group(1))
        return None

for team in teams:
    print(f"\n🔹 Récupération des données pour {team}...")
    for game in games:
        url = f"https://liquipedia.net/{game}/{team}/Results"
        try:
            tables = pd.read_html(url)
        except:
            print(f"⚠️ Impossible de récupérer la page pour {team} sur {game}")
            continue

        found_data = False
        for i, table in enumerate(tables):
            date_cols = [c for c in table.columns if "Date" in c or table[c].astype(str).str.contains(r"20\d{2}").any()]
            if date_cols:
                col = date_cols[0]
                table["Year"] = table[col].apply(extract_year)
                table = table[table["Year"].notna()]

                for year in table["Year"].unique():
                    count = table[table["Year"] == year].shape[0]
                    all_data.append({
                        "Team": team.replace("_"," "),
                        "Year": int(year),
                        "Game": game,
                        "TournamentsPlayed": int(count)
                    })
                found_data = True

        if found_data:
            print(f"✅ Données récupérées pour {team} sur {game}")
        else:
            print(f"⚠️ Aucun tableau valide pour {team} sur {game}")
        time.sleep(1)

final_df = pd.DataFrame(all_data)

if not final_df.empty:
    games_active = final_df.groupby(["Team","Year"])["Game"].nunique().reset_index().rename(columns={"Game":"GamesActive"})
    tournaments_sum = final_df.groupby(["Team","Year"])["TournamentsPlayed"].sum().reset_index()
    final_summary = pd.merge(games_active, tournaments_sum, on=["Team","Year"])
    final_summary.to_csv("esports_dataset.csv", index=False)
    print("\n✅ Dataset final créé : esports_dataset.csv")
    print(final_summary)
else:
    print("⚠️ Aucune donnée récupérée.")