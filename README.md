# Webcrawler

Crawler using python

## Features
- Capable of using LIFO and FIFO queue (DFS and BFS)
- Can be run using a beam search 
- Implemented as a graph search (nodes will not be visited twice).
- **Robust** : will not get stuck in spider traps due to being implemented as graph search.
- **Polite** : pause between request.

## How it works: closer look at crawl_bfs_graph_search

Here is a Quick overview (pseudocode)of how the crawler works.




>
    crawl_bfs_graph_search(seed , max):     // assuming no other argument is needed
        node_visited = 0 
        visited = {}
        website_graph = dict()              // adjacency list  representing a graph 
        frontier =  [seed\]                 // FIFO queue of url that need exploring scheduler 

        while (frontier!= [] and node_visited< max)
            {
            curr = frontier.pop()           // pop the oldest element still in the list
            links = curr.extract_valid_linkt()      //extract all links in the same domain as the seed
            frontier.add(links) //add all links to frontier

            website_graph[curr\] = { ref : links, name: page_title} // other features can be added to each page.
            }

        return website_graph, visited       


## Files 
* `Crawler.py`: logic of the crawler. contain 2 different scheduler(FIFO, LIFO) each can be *polite*/*impolite*, *use beam search* / *not use beam search* 
* `requirements.txt`: packages that need installation
* `main.py`: exectue crawling using Crawler.py and saving the result

## Future Improvement

- Visualize the connections
- Respecting robots.txt
- Support multiprocessing (to crawl multiple websites).
- Implement [mercator](https://link.springer.com/article/10.1023/A:1019213109274) crawler:
- Add functionality for scraping the data.

