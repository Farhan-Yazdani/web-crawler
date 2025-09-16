from Crawler import crawl_bfs_graph_search
import json



seed_url = 'https://openweathermap.org/'


G, v = crawl_bfs_graph_search(target_url=seed_url, max_visited=10, politeness=True)

name = 'weathermap'
with open(f'examples/WEB_GRAPH_{name}.json', 'w') as f:
    json.dump(G, f, indent=4) 



with open(f'examples/set_of_visited_pages_{name}.txt', 'w') as f:
    for item in v:
        f.write(item + '\n') # since the is not ordered the order of visitation will change. true order can be extracted via graph of website


