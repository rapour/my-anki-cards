In computer science, what is a **graph**, and what do the words **node**, **edge**, **weight** and **path** mean? Use currency conversion as the example.

---

A graph is a way of describing a set of things and the connections between them. It is the standard tool for any problem that says "can I get from here to there?".

- **Node** (also called a *vertex*): one of the things. In currency conversion, each currency (USD, EUR, CAD) is a node.
- **Edge**: a connection between two nodes. The quote "1 USD = 1.3 CAD" is an edge from USD to CAD.
- **Weight**: a number attached to an edge. Here the weight is the exchange rate, 1.3. In a shipping problem the weight would be the price of that leg.
- **Directed or undirected**: a directed edge only works one way (USD to CAD). An undirected edge works both ways. For currencies we usually add the way back ourselves, as an edge from CAD to USD with weight 1/1.3.
- **Path** (or *route*): a sequence of nodes where each neighbouring pair is joined by an edge, such as EUR, USD, CAD.

```
EUR --1.1--> USD --1.3--> CAD
```

To turn EUR into CAD you walk the path EUR, USD, CAD and multiply the weights along the way: 1.1 × 1.3 = 1.43.

**How a graph is stored.** The most common way is an *adjacency list*: for every node, a list of its neighbours (and the weight of each edge). In Rust that is a `HashMap<&str, Vec<(&str, f64)>>`, or a `Vec<Vec<usize>>` when nodes are numbered 0, 1, 2 and so on.

**Two letters used in every complexity card:** `V` is the number of nodes (vertices) and `E` is the number of edges.
