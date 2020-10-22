# _Google’s PageRank estimation_
Harold Fellermann

-----------
### Case Study 5
This case study introduces you to working with graphs. Graphs are important data structures in computer science and are a useful tool for a wide variety of problems. They will be formally introduced in the math lectures next term, but since they are rather intuitive as well as fun to work with, I decided to already present them to you in this exercise.

Here, we will work with a graph that represents the link structure of the web site of Newcastle University. In this graph, every node represents a web page, labeled with its URL. A directed edge from node A to node B signifies that page A holds a link to page B.

#### Learning outcomes
In particular, you will learn

* How to represent and operate over graphs in python
* How to translate pseudo code into executable programmes
* How to implement an estimate of Google’s PageRank index
-----------

### PageRank
How does Google decide which pages to show you for a particular search? Obviously, the pages it displays should feature the search terms of your query, but apart from that, how does Google generally manage to put relevant websites at the top of the search results? The answer to this is in a concept called “PageRank”, named after one of its inventors, Larry Page, co-founders of Google Inc.

According to PageRank, a web page is relevant if other relevant pages link to it. While intuitive, this recursive definition does not appear to be very helpful. After all, to determine the PageRank of a web page, I would already need to know the PageRanks of all the pages that link to it. And to determine these other ranks, I need to know the rank of the pages that link to them… The calculation does not seem to ever end. But it turns out that we can get out of this conundrum by using simple tricks.

### PageRank estimation through random walkers
Image a web surfer eagerly browsing the web for some piece of information. Before the age of modern day search engines, she would start her search at some web page, from were she would click link after link after link to get to her desired target. The path that she takes through the web is thereby partly determined by the links that web content creators had put in their pages, partly by the surfer’s interests that influence which of those links she follows.

Again prior to the age of the modern internet, search engine providers had little information about specific user behavior. All they got was the information provided by web authors about which page links to which other page. In the lack of information about user behavior, we can just as well assume that the surfer would randomly choose one of the links to follow.

If we now take a big number of these random surfers, each of them will create her own random path through the web. However, since the possible routes they can take have been pre-selected by the content creators, it is more likely that their random search ends on a page that can be reached from many different nodes – particularly if those nodes can also be easily reached as well. It is now not too far-fetched to assume that those pages contain relevant information, as otherwise content creators would not have linked to them.

We can formalize this thought process into a recipe (or algorithm) that estimates PageRank through random walks. The algorithm is written in pseudo code as:

```
initialize hit_count[node] with 0 for all nodes
repeat n_iterations times:
    current_node <- randomly selected node
    repeat n_steps times:
       current_node with <- randomly chosen node among the out edges of current_node
    hit_count[current_node] += 1/n_iterations
```
    
The fraction of times that a certain web page is hit is an estimate for its PageRank. The more random surfers are used for the calculation the better the estimate.

### PageRank estimation through probability distributions
In the last method, we have seen that the PageRank is the probability to reach a page through a random walk. We have estimated this probability by measuring the frequency with which a page is hit. The downside of this approach is that we need to run many repetitions in order for these frequencies to accurately approximate probabilities. This has a large computational cost. Can we do better?

It turns out we can. Instead of following single instances of random surfers through the web, we could follow the probability that a random surfer is currently on some page. Imagine we know that the surfer were currently on a specific page, and that this page has an out degree of k, we can then conclude that—after following a single link—she will be on any of these k pages with probability 1/k.

To achieve the same model of random surfers that we used in the previous section, we need to make sure that surfers start their walk on a random page. So the initial probability distribution is uniform (that means: the same) among all nodes. If the graph features n nodes, the initial probability to be at any node is 1/n.

In general, by following a link from one node to another, the probabilty of having been at the current node is devided by the number of edges that lead out of that node and the resulting value is added to the probability of being at the target node in the next step.

Although probabilities of being on a certain page change with each iteration, it can be shown that (under some conditions that are usually fulfilled for real-world graphs) these changes are expected to become smaller and smaller with each iteration: The probability that a certain node is left through one of its out-edges is compensated by the probability that the node is entered through one of its in-edges. After several iterations, the probabilities do not change significantly any more.

We can formalize this revised procedure in the following pseudo code:

```
initialize node_prob[node] = 1/(number of nodes) for all nodes
repeat n_iterations times:
    initialize next_prob[node] = 0 for all nodes
    for each node:
        p <- node_prob[node] divided by its out degree
        for each target among out edges of node:
            next_prob[target] += p
    node_prob <- next_prob
```

### Disclaimer
I want to disclose that the real PageRank algorithm published by Larry Page and Sergei Brin is slightly more complicated than what has been described before. There are some corner cases that need to be considered. For example, what should be done if a page does not contain any links? Also, the second scenario would incorporate probabilities for the surfer to stop browsing and/or start a new search. The real algorithm includes these scenarios, but the ones given above are good enough for the following exercise.

------------------------

### Assignment 5
For this assignment, I have created a python project for you on nucode which you can see at https://nucode.ncl.ac.uk/scomp/stage1/csc1034/practicals/practical-5. You should fork this project as we did in the previous practicals, so that you have your own copy and then clone it into your local environment so that you can edit it.

The project comes with a file school_web.txt which contains information about links among web page of the School of Computing website. In this file, each line contains two URLs seperated by a space, for example:

http://www.ncl.ac.uk/computing/ http://www.ncl.ac.uk/computing/induction/
This means that the page /computing/ links ot the page /computing/induction/.

The file page_rank.py contains some boiler plate code. In particular, the main() function calls the functions read_graph to read in the website structure from a text file and print_stats to print the number of nodes and edges in the graph. It then calls the functions stochastic_page_rank and distribution_page_rank and displays the top ranked pages together with their PageRank. These four functions exist in the code, but currently only raise a RuntimeError when called.

Your job is to implement the functions such that read_graph returns some python object that contains the graph data. stochastic_page_rank should implement the first method explained above to estimate PageRanks via random walkers, whereas distribution_page_rank should implement the second method to estimate PageRanks via probability ditributions. The functions that estimate PageRanks have to follow exactly the behaviour specified by the above pseudo code definitions.

It is up to you to decide how you want to store the graph data in python. You can use one of the ways presented in the lectures (e.g. by implementing a Graph class, using a third party graph class, or using builtin python types such as dictionaries) or explore your own ways. You are allowed to add more functions or modules to the project, as long as you do not change the signature of the four functions called in main.

As always, ensure that your code is nicely structured and sufficiently commented.

### Marking Criteria
An upper second solution

* correctly implements both algorithms
* has its code arranged in a nice structure by making appropriate use of modules, classes and or functions
* provides a decent amount of documentation and comments to explain the implementation
* makes use of isolated commits with clear commit messages
