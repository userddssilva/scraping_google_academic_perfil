import requests
import re

from pprint import pprint
from time import sleep
from bs4 import BeautifulSoup

import matplotlib.pyplot as plt
import networkx as nx   

# https://scholar.google.com.br/citations?hl=pt-BR&user=OXYNcyoAAAAJ

def read_page_perfil():
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
            print("Invalid Request, trying again in 10s")
            sleep(10)

def rename_authors(authors):
    authors = list(map(lambda b: b.replace("FG de Sousa Pires","F Pires"), authors))
    authors = list(map(lambda b: b.replace("KB Teixeira","K Teixeira"), authors))
    return authors

def get_year(result, paper_name):
    try:
        year = int(result.contents[2].contents[0].contents[0])
        return year
    except:
        year = 0
        print("The paper:", paper_name, ", no has year")
        return year

def extract_inf_perfil(results):
    paper_graph = {}
    # p, n = "A", 1
    for result in results:
        paper_name = result.contents[0].contents[0].contents[0]
        authors = str(result.contents[0].contents[1].contents[0]).split(", ")
        year = get_year(result, paper_name)
        authors = rename_authors(authors)
        if year >= 2017:
            # paper_number = p + str(n)
            # n += 1 
            paper_graph[paper_name] = authors

    # pprint(paper_graph)
    return paper_graph

def generate_authors_graph(graph):
    # Creating graph
    G = nx.Graph()

    # creanting edges
    for paper in graph.keys():
        for author in graph[paper]:
            G.add_edge(paper, author)

    # define size image
    plt.figure(figsize=(50, 70))
    nx.draw(G, with_labels=True)
    # plt.savefig("artigos_com_nome.png") # save as png
    # plt.savefig("artigos_com_sigla.png") # save as png
    plt.show() # display

def main():
    # online
    # page = request_page()
    # offline
    page = read_page_perfil()

    soup = BeautifulSoup(page,  "html.parser")

    results = soup.find_all(class_="gsc_a_tr")

    g = extract_inf_perfil(results)

    generate_authors_graph(g)


if __name__ == "__main__":
    main()
    