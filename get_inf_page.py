import requests
import re

from pprint import pprint
from time import sleep
from bs4 import BeautifulSoup

import matplotlib.pyplot as plt
import networkx as nx   

# https://scholar.google.com.br/citations?hl=pt-BR&user=OXYNcyoAAAAJ

def make_html():
    page = ""
    with open("fernanda_pires.html", "r") as fl:
        for line in fl:
            page += line + "\n"
    return page

def request_page():
    page = None
    while page == None:
        try:
            url = "https://scholar.google.com.br/citations?hl=pt-BR&user=OXYNcyoAAAAJ"
            page = requests.get(url)
            return page
        except:
            print("Invalid Request, try again in 10s")
            sleep(10)

def clean_authors(authors):
    authors = list(map(lambda b: b.replace(" FG de Sousa Pires","F Pires"), authors))
    authors = list(map(lambda b: b.replace("FG de Sousa Pires","F Pires"), authors))
    authors = list(map(lambda b: b.replace("KB Teixeira","K Teixeira"), authors))
    authors = list(map(lambda b: b.replace(" K Teixeira","K Teixeira"), authors))
    return authors

if __name__ == "__main__":
  
    # page = request_page()
    page = make_html()
    soup = BeautifulSoup(page,  "html.parser")

    # Creating graph
    G = nx.Graph()
    #G1 = nx.Graph()

    ## Extracting info of page
    results = soup.find_all(class_="gsc_a_tr")
    p = "A"
    n = 1
    for result in results:
        paper_name = result.contents[0].contents[0].contents[0]
        authors = str(result.contents[0].contents[1].contents[0]).split(", ")
        try:
            year = int(result.contents[2].contents[0].contents[0])
        except:
            year = 0
            print("The paper:", paper_name, ", no has year")

        if year >= 2017:
            paper_number = p + str(n)
            n += 1
            
            authors = clean_authors(authors)

            print(authors)

            # creanting edges
            for author in authors:
                G.add_edge(paper_name, author)
                #G1.add_edge(paper_number, author)

    nx.draw(G, with_labels=True)
    # nx.draw(G1, with_labels=True)
    plt.savefig("artigos_com_nome.png") # save as png
    #plt.savefig("artigos_com_sigla.png") # save as png
    plt.show() # display
    ## Extracting all author names: