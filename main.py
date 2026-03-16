import cloudscraper
from bs4 import BeautifulSoup
import pandas as pd

URL = "https://royaleapi.com/clan/QGV8L8P0/war/analytics"

scraper = cloudscraper.create_scraper()
resp = scraper.get(URL)

if resp.status_code != 200:
    print("Erreur HTTP", resp.status_code)
    exit()

soup = BeautifulSoup(resp.text, "html.parser")

table = soup.find("table")
if not table:
    print("Tableau non trouvé dans la page.")
    exit()

for row in table.find_all("tr"):
    if row.find("i", class_="small circle outline fitted icon"):
        row.decompose()

df = pd.read_html(str(table))[0]

df['ratio P'] = df['P'].str.split('/').apply(lambda x: float(x[0]) / float(x[1]) if len(x) == 2 and float(x[1]) != 0 else 0)

cols_to_drop = [col for col in df.columns if col.startswith('12')]
cols_to_drop = cols_to_drop[3:]
df = df.drop(columns=cols_to_drop, errors='ignore')
df = df.drop(columns=['M'], errors='ignore')

print("\n=== Tableau filtré ===")
print(df)
