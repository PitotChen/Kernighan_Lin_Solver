import networkx as nx

def calculate_d_values(G, partition_a, partition_b):
    d_values = {}
    for node in G.nodes:
        d_values[node] = sum(G.nodes[neighbor]['partition'] != G.nodes[node]['partition']
                             for neighbor in G[node])
        if G.nodes[node]['partition'] == 'A':
            d_values[node] -= sum(1 for neighbor in G[node] if neighbor in partition_a)
        else:
            d_values[node] -= sum(1 for neighbor in G[node] if neighbor in partition_b)
    return d_values

def find_best_swap(G, d_values, partition_a, partition_b):
    best_gain = -float('inf')
    best_pair = None
    for node_a in partition_a:
        for node_b in partition_b:
            if (node_a, node_b) not in G.edges: 
                gain = d_values[node_a] + d_values[node_b]
            else: 
                gain = d_values[node_a] + d_values[node_b] - 2
            if gain > best_gain:
                best_gain = gain
                best_pair = (node_a, node_b)
    return best_pair, best_gain

def generate_gain_table(G, partition_a, partition_b, d_values):
    gain_table = {}
    for node_a in partition_a:
        for node_b in partition_b:
            if (node_a, node_b) not in G.edges: 
                gain = d_values[node_a] + d_values[node_b]
            else: 
                gain = d_values[node_a] + d_values[node_b] - 2
            gain_table[(node_a, node_b)] = gain
    return gain_table

edges = [
    (1, 2), (1, 3), (1, 6), (2, 4), (2, 7), (3, 4),
    (3, 5), (3, 6), (3, 8), (4, 6), (5, 7), (5, 8), (5, 9),
    (5, 10), (7, 8), (8, 9), (8, 10), (9, 10)
]

G = nx.Graph()
G.add_edges_from(edges)

partition_a = [1, 2, 3, 4, 5]
partition_b = [6, 7, 8, 9, 10]

# partition information node attributes
for node in partition_a:
    G.nodes[node]['partition'] = 'A'
for node in partition_b:
    G.nodes[node]['partition'] = 'B'

d_values = calculate_d_values(G, partition_a, partition_b)
initial_partition_cost = sum(1 for edge in G.edges
                             if G.nodes[edge[0]]['partition'] != G.nodes[edge[1]]['partition'])

best_swap, best_gain = find_best_swap(G, d_values, partition_a, partition_b)
initial_gain_table = generate_gain_table(G, partition_a, partition_b, d_values)


if best_swap:
    node_a, node_b = best_swap
    partition_a.remove(node_a)
    partition_b.remove(node_b)
    partition_a.append(node_b)
    partition_b.append(node_a)
    G.nodes[node_a]['partition'] = 'B'
    G.nodes[node_b]['partition'] = 'A'


new_d_values = calculate_d_values(G, partition_a, partition_b)
new_gain_table = generate_gain_table(G, partition_a, partition_b, new_d_values)
new_partition_cost = sum(1 for edge in G.edges
                         if G.nodes[edge[0]]['partition'] != G.nodes[edge[1]]['partition'])

print("Initial partition cost:", initial_partition_cost)
print("New partition cost after swap:", new_partition_cost)
print("Initial D values:", d_values)
print("New D values after swap:", new_d_values)
print("Best swap:", best_swap)
print("Best gain:", best_gain)
print("Initial Gain Table:", initial_gain_table)
print("New Gain Table after swap:", new_gain_table)
