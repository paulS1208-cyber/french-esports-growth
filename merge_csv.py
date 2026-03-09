import pandas as pd

csv1 = pd.read_csv("esports_summary.csv", sep=";")
csv2 = pd.read_csv("Team_PrizeMoney.csv", sep=";")

# Vérifions les colonnes
print(csv1.columns)
print(csv2.columns)

# Fusionner
merged = pd.merge(csv1, csv2, on=["Team","Year"], how="outer")  # si tu n'as pas Game dans les 2 fichiers
merged.to_csv("merged_esports.csv", index=False, sep=";")
print("✅ Fusion réussie !")