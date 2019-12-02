import os
import time
from collections import defaultdict
from progress import Progress
import random

WEB_DATA = os.path.join(os.path.dirname(__file__), 'school_web.txt')


def load_graph(fd):
    """Load graph from text file

    Parameters:
    fd -- a file like object that contains lines of URL pairs

    Returns:
    A representation of the graph.

    Called for example with

    >>> graph = load_graph(open("web.txt"))

    the function parses the input file and returns a graph representation.
    Each line in the file contains two white space separated URLs and
    denotes a directed edge (link) from the first URL to the second.
    """
    # create an empty list for pairs of (node, target) which will depict the connection of URLs
    connections = []
    edges = []
    # Iterate through the file line by line
    for line in fd:
        # And split each line into two URLs
        node, target = line.split()
        # take a pair of node and target from the same line and append to the list of connection pairs
        connections.append([node, target])

    # create an empty temporary dictionary using collections' defaultdict which will store values in lists
    temp_d = defaultdict(list)
    # iterate through connections, integrate repeating nodes into single keys
    # and store all their targets as a list of values
    for k, v in connections:
        temp_d[k].append(v)
    # turn the temporary dictionary into a final dictionary with values stored in lists
    graph_rep_list = dict((k, list(v)) for k, v in temp_d.items())

    return graph_rep_list


def print_stats(graph_rep_list):
    """Print number of nodes and edges in the given graph"""
    # calculate the number of keys in the dictionary which is the number of distinctive nodes in the graph
    nodes = len(graph_rep_list.keys())
    print(f'There are {nodes} nodes in the graph.')

    # calculate the total number of values in the dictionary which represents the number of edges in the the graph
    edges = 0
    for key, value in graph_rep_list.items():
        edges += len(list(value))
    print(f'There are {edges} edges in the graph.')


def stochastic_page_rank(graph_rep_list, n_iter=1_000_000, n_steps=100):
    """Stochastic PageRank estimation

    Parameters:
    graph -- a graph object as returned by load_graph()
    n_iter (int) -- number of random walks performed
    n_steps (int) -- number of followed links before random walk is stopped

    Returns:
    hit_count -- A dict that assigns each page its hit frequency

    This function estimates the Page Rank by counting how frequently
    a random walk that starts on a random node will after n_steps end
    on each node of the given graph.
    """
    # create a dictionary to save the pages and their hit frequencies to
    hit_count = {}
    # add each node from the graph to the hit_count dictionary and set their hit frequencies to 0.
    for key in graph_rep_list.keys():
        hit_count[key] = 0

    # for each random walker, choose a random website to start from
    for i in range(n_iter+1):
        # by choosing a random node from the starting nodes in the graph
        current_node = random.choice(list(graph_rep_list.keys()))
        # for every step taken by the walker before reaching the end URL:
        for j in range(n_steps+1):
            # the walker randomly enters one of the URLs from the starting/current node's targets
            current_node = random.choice(list(graph_rep_list[current_node]))
        # up the hit count for the current node
        hit_count[current_node] += 1/n_iter
        # update the hit_count dictionary with this upped hit frequency
        hit_count.update({current_node: hit_count[current_node]})
    return hit_count


def distribution_page_rank(graph_rep_list, n_iter=100):
    """Probabilistic PageRank estimation

    Parameters:
    graph -- a graph object as returned by load_graph()
    n_iter (int) -- number of probability distribution updates

    Returns:
    node_prob -- A dict that assigns each page its probability to be reached

    This function estimates the Page Rank by iteratively calculating
    the probability that a random walker is currently on any node.
    """
    # create an empty dictionary to store the pages and their probabilities of being reached in
    node_prob = {}
    # set the probabilities of the walker starting on any of the nodes in the graph
    for key in graph_rep_list.keys():
        node_prob[key] = 1/len(graph_rep_list.keys())

    # create another empty dict to temporarily store the probability of reaching the subsequent node after current one
    next_prob = {}
    # for each step in the walker's walk
    for i in range(n_iter + 1):
        # initially set the probability of reaching the subsequent node to 0 for all nodes
        for key in graph_rep_list.keys():
            next_prob[key] = 0
        # for each node create the method of counting the probability of being on it
        for key in graph_rep_list.keys():
            p = node_prob[key] / len(graph_rep_list[key])
            # for each target update its hit probability by adding the p (probability counter)
            for value in graph_rep_list[key]:
                next_prob[value] += p
        # update the general dict with new probability values from the temporary dict
        node_prob.update(next_prob)

    return node_prob


def main():
    # Load the web structure from file
    web = load_graph(open(WEB_DATA))

    # print information about the website
    print_stats(web)

    # The graph diameter is the length of the longest shortest path
    # between any two nodes. The number of random steps of walkers
    # should be a small multiple of the graph diameter.
    diameter = 3

    # Measure how long it takes to estimate PageRank through random walks
    print("Estimate PageRank through random walks:")
    n_iter = len(web)**2
    n_steps = 2*diameter
    start = time.time()
    ranking = stochastic_page_rank(web, n_iter, n_steps)
    stop = time.time()
    time_stochastic = stop - start

    # Show top 20 pages with their page rank and time it took to compute
    top = sorted(ranking.items(), key=lambda item: item[1], reverse=True)
    print('\n'.join(f'{100*v:.2f}\t{k}' for k, v in top[:20]))
    print(f'Calculation took {time_stochastic:.2f} seconds.\n')

    # Measure how long it takes to estimate PageRank through probabilities
    print("Estimate PageRank through probability distributions:")
    n_iter = 2*diameter
    start = time.time()
    ranking = distribution_page_rank(web, n_iter)
    stop = time.time()
    time_probabilistic = stop - start

    # Show top 20 pages with their page rank and time it took to compute
    top = sorted(ranking.items(), key=lambda item: item[1], reverse=True)
    print('\n'.join(f'{100*v:.2f}\t{k}' for k, v in top[:20]))
    print(f'Calculation took {time_probabilistic:.2f} seconds.\n')

    # Compare the compute time of the two methods
    speedup = time_stochastic/time_probabilistic
    print(f'The probabilistic method was {speedup:.0f} times faster.')


if __name__ == '__main__':
    main()
