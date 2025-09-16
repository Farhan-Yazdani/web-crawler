from time import sleep
import random # can be used to be more respectful towards the page and send slower request. also reduce the chance of getting blocked


import requests
from bs4 import BeautifulSoup




def crawl_bfs_graph_search(target_url: str , max_visited: int =50, beam_size = -1, politeness: bool = False ):
    '''
        crawl a url using a FIFO queue until. stop after a certain iteration.

        BFS graph search implemented with possiblity of beam searcch

        Args: 
            target_url (str): saem as seed_url
            max_visited (int): specify when to stop the crawl.
            beam_size (int): if a positve intger perform beam search with beam_size specified
            politeness (bool): if true, wait for a while before sending another request
        Returns:
            (graph , visited_set)    
    '''
    

    # initialize the list of discovered URLs
    frontier = [target_url]


    # request the target URL
    response = requests.get(target_url , verify = False)
    response.raise_for_status() 


    # parse the HTML
    soup = BeautifulSoup(response.text, "html.parser")

    # collect all the links
    link_elements = soup.select("a[href]")

    G = dict() # graph of the connections

    crawl_count = 0

    visited = set()

    while frontier and (crawl_count < max_visited):

        if(beam_size >= 0 ): frontier = frontier[:beam_size] # cut the frontier if we are to use beam search
        current_url = frontier.pop(0)
    
        # request the target URL
        response = requests.get(current_url, verify = False)
        
        if (response.status_code != 200):
            visited.add(current_url)
            crawl_count += 1 # still considered expanded
            G[current_url] = _construct_dict_value(current_url,soup) # {'name': soup.title.string ,'ref':[] }
            continue


        # parse the HTML
        soup = BeautifulSoup(response.text, "html.parser")

        # collect all the links
        link_elements = soup.select("a[href]")

        G[current_url] = _construct_dict_value(current_url,soup) # {'name': soup.title.string ,'ref':[] }

        if politeness : sleep(0.15 + random.randint(1,3)*0.1)

        for link_element in link_elements:
            url = link_element["href"]
            

            if not url.startswith("http"):
                absolute_url = requests.compat.urljoin(target_url, url)
            else:
                absolute_url = url

            
            # ensure the crawled link belongs to the target domain and hasn't been visited
            if (
                absolute_url.startswith(target_url)
                and absolute_url not in visited
               
            ):
                frontier.append(absolute_url)
                G[current_url]['ref'].append(absolute_url)

        visited.add(current_url)


        crawl_count += 1   # this way crawl count mean the number of nodes visited. if we mode the line inside the loop it will mean the number of nodes generated.

    return G, visited


def crawl_dfs_tree_search(target_url:str , max_visited: int = 50, beam_size = -1, politeness: bool = False ):
    '''
        crawl a url using a FIFO queue until a specified depth.

        DFS tree search implemented with possiblity of beam search. i.e the visited set is not implemented and frontier can be of limited size.

        Args: 
            target_url (str): saem as seed_url
            max_visited (int): specify when to stop the crawl.
            beam_size (int): if a positve intger perform beam search with beam_size specified
            politeness (bool): if true, wait for a while before sending another request
        Returns:
            dict: adj list representign the graph of the website
    '''

    

    # initialize the list of discovered URLs
    frontier = [target_url]


    # request the target URL
    response = requests.get(target_url , verify = False)
    response.raise_for_status() 


    # parse the HTML
    soup = BeautifulSoup(response.text, "html.parser")

    # collect all the links
    link_elements = soup.select("a[href]")

    G = dict() # graph of the connections

    crawl_count = 0

    

    while frontier and (crawl_count < max_visited):

        if(beam_size >= 0 ): frontier = frontier[:beam_size] # cut the frontier if we are to use beam search
        current_url = frontier.pop() # reurrn the last element in the list
    
        # request the target URL
        response = requests.get(current_url , verify = False)
        
        if (response.status_code != 200):
            
            crawl_count += 1 # still considered expanded
            G[current_url] = _construct_dict_value(current_url,soup) # often same as {'name': soup.title.string ,'ref':[] }
            continue

        # parse the HTML
        soup = BeautifulSoup(response.text, "html.parser")

        # collect all the links
        link_elements = soup.select("a[href]")

        G[current_url] = _construct_dict_value(current_url,soup)
        if politeness:  sleep(0.15 + random.randint(1,3)*0.1)

        for link_element in link_elements:
            url = link_element["href"]
            

            if not url.startswith("http"):
                absolute_url = requests.compat.urljoin(target_url, url)
            else:
                absolute_url = url

            
            # ensure the crawled link belongs to the target domain and hasn't been visited
            if absolute_url.startswith(target_url):
                frontier.append(absolute_url)
                G[current_url]['ref'].append(absolute_url)

        

        crawl_count += 1   # this way crawl count mean the number of nodes visited. if we mode the line inside the loop it will mean the number of nodes generated.

    return G


def _construct_dict_value(url, soup):
    '''
    util function return the initialized value for a node in website graph.
    If a page has no title no url will be set to be the name
    '''
    try:
        len(soup.title.string)>1

    except Exception:
        return {'name':url  ,'ref':[] }

    return {'name': soup.title.string ,'ref':[] }

