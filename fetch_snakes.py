import requests
import xml.etree.ElementTree as ET
import time

def fetch_name(tid):
    url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    params = {
        "db": "taxonomy",
        "id": tid,
        "retmode": "xml"
    }

    for _ in range(5):
        try:
            r = requests.get(url, params=params, timeout=10)
            text = r.text.strip()

            if not text.startswith("<"):
                time.sleep(0.1)
                continue

            root = ET.fromstring(text)
            sci = root.find(".//ScientificName")
            if sci is not None:
                return sci.text
        except Exception:
            time.sleep(0.1)

    return None

with open("taxids.txt") as f:
    ids = [line.strip() for line in f]

out = open("snake_species_raw.txt", "w", encoding="utf-8")

for i, tid in enumerate(ids, 1):
    name = fetch_name(tid)
    if name:
        out.write(name + "\n")

    if i % 100 == 0:
        print(f"Fetched {i}/{len(ids)}")

out.close()
print("Done.")

