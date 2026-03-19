from bs4 import BeautifulSoup

with open("/tmp/rice_depts.html", "r") as f:
    soup = BeautifulSoup(f, "html.parser")

links = set()
for a in soup.find_all("a", href=True):
    href = a["href"]
    if ".rice.edu" in href and "engineering.rice.edu" not in href:
        links.add(href)

for link in sorted(links):
    print(link)
