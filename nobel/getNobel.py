from bs4 import BeautifulSoup
import urllib.request
import pickle

opener = urllib.request.FancyURLopener({})
people = []

# url tabulky
tableurl = "https://en.wikipedia.org/wiki/List_of_Nobel_laureates"
baseurl = "https://en.wikipedia.org"
# hlavicka tabulky
header = ["year", "phys", "chem", "med", "lit", "peace", "econ"]

# ziskani odkazu na vsechny laureaty
f = opener.open(tableurl)
content = f.read()
soup = BeautifulSoup(content, "html.parser")
year = "0"
for row in soup.find("table", {"class": "wikitable sortable"}).findAll("tr"):
    cells = row.findAll("td")
    for i, cell in enumerate(cells):
        h = header[i]
        if h == "year":
            year = str(cell.string)
            continue
        for a in cell.findAll("a"):
            href = str(a["href"])
            if href[:6] == "/wiki/":
                name = str(a["title"])
                people.append({"year": year, "sub": header[i], "name": name, "href": baseurl + href})

print("Found", len(people), "laureates")


def getBirthDate(url):
    """zjisti den narozeni z adresy na wikipedii"""
    f = opener.open(url)
    content = f.read()
    soup = BeautifulSoup(content, "html.parser")
    bday = soup.find("span", {"class": "bday"})
    if bday is not None:
        return str(bday.string)
    else:
        return None

# llide bez dne narozeni
noBD = []

for person in people:
    print("% 30s" % person["name"], "was born ", end="")
    bdate = getBirthDate(person["href"])
    person["bdate"] = bdate
    if bdate is None:
        noBD.append(person)
    print(bdate)

print()
print("Found", len(noBD), "people with no birth date")

# ulozeni na pozdejsi zpracovani
with open("people.pickle", "wb") as fpick:
    pickle.dump(people, fpick)
