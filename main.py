import requests
from bs4 import BeautifulSoup
import pandas as pd

URL = "https://royaleapi.com/clan/QGV8L8P0/war/analytics"

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "en-US,en;q=0.9",
}

resp = requests.get(URL, headers=headers)
if resp.status_code != 200:
    print("Erreur HTTP", resp.status_code)
    exit()

soup = BeautifulSoup(resp.text, "html.parser")

# On cherche le premier tableau sur la page
table = soup.find("table")
if not table:
    print("Tableau non trouvé dans la page.")
    exit()

# Lire le tableau avec pandas (beau/borde de HTML)
df = pd.read_html(str(table))[0]

# Montre les premières lignes

df['ratio P'] = df['P'].str.split('/').apply(lambda x: float(x[0]) / float(x[1]) if len(x) == 2 and float(x[1]) != 0 else 0)
# Supprime toutes les colonnes qui commencent par '12' sauf les 3 premières et M
cols_to_drop = [col for col in df.columns if col.startswith('12')]
cols_to_drop = cols_to_drop[3:]  # Garde les 3 premières
df = df.drop(columns=cols_to_drop, errors='ignore')
df = df.drop(columns=['M'], errors='ignore')

print("\n=== Tableau filtré ===")
print(df)
