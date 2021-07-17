import pandas as pd # pandas library useful for manipulating files
import networkx as nx
import random as rnd # for random number generation and random shuffling/sampling
import numpy as np # library for numerical functions

##############################################################
# THIS FUNCTION READS NODE ATTRIBUTES FROM A FILE AND ADDS
#  THEM TO A NETWORKX GRAPH
def get_degree_list(network):

    return list(dict(network.degree()).values())

##############################################################
# THIS FUNCTION READS NODE ATTRIBUTES FROM A FILE AND ADDS
#  THEM TO A NETWORKX GRAPH
def add_node_attribute_from_file(network, filename, label):
    
    # make a copy of the network before making any changes (as the original network will be rewritten)
    new_network = network.copy()
    
    # read the file with node attributes as a pandas dataframe(format: node, node attribute value)
    attribs = pd.read_csv(filename, names = ['node', 'val'])
    
    # convert pandas dataframe to dictionary
    attrib_dict = pd.Series(attribs.val.values,index=attribs.node).to_dict()
    
    # use dictionary to add node attributes to networkx network 
    #  (new_network is edited in place)
    nx.set_node_attributes(new_network, attrib_dict, label)
        
    return new_network

#############################################################
# THIS FUNCTION FINDS ALL NODES WITH A GIVEN NODE ATTRIBUTE
def find_nodes_with_attribute(network, attributename, attributevalue):
    
    list_nodes = [node for node,val in network.nodes(data=True) if val[attributename]==attributevalue]
    
    return list_nodes

#############################################################
# THIS FUNCTION RETURNS A LIST OF THE NODE ATTRIBUTE VALUES 
#  FOR THE PROVIDED attributename
def get_node_attributes_list(network, attributename):
    
    return list(nx.get_node_attributes(network, attributename).values())

##############################################################
# THIS FUNCTION TAKES IN A LIST OF VALUES AND RETURNS A DICTIONARY OF THE 
#  FREQUENCY/PROBABILITY DISTRIBUTION OF THOSE VALUES
def get_distribution(list_values):
    
    counts = np.bincount(list_values)
    
    vals = counts/sum(counts)
    keys = range(0,max(list_values)+1)
    
    return dict(zip(keys,vals))

#############################################################
# THIS FUNCTION SHUFFLES ALL THE VALUES IN A DICTIONARY 
#  (e.g. it can shuffle all the node attributes in a network)
def shuffle_dict(mydict):
    
    keys = list(dict(mydict).keys())
    vals = list(dict(mydict).values())
    
    rnd.shuffle(vals)

    return dict(zip(keys,vals))

#############################################################
# THIS FUNCTION RETURNS THE SPECIFIED NUMBER OF NODES (num_wanted_nodes)
#  OF HIGHEST DEGREE IN THE NETWORK (mynet)
def find_highest_degree_nodes(mynet, num_wanted_nodes):
    
    sorted_deg_dict = sorted(mynet.degree, key=lambda x: x[1], reverse=True)
    
    wanted_dict = sorted_deg_dict[0:num_wanted_nodes]
    
    wanted_nodes = [node for node,deg in wanted_dict]

    return wanted_nodes

#############################################################
# THIS FUNCTION CALCULATES THE DIAMTER OF THE NETWORK (mynet)
#  IF THE NETWORK IS UNCONNECTED IT PROVIDES THE DIAMTER OF THE
#  LARGEST CONNECTED COMPONENT
def calc_diameter(mynet):
    
    if nx.is_connected(mynet):
        return(nx.diameter(mynet))
    else:
        comp_sorted_bysize = sorted(nx.connected_components(mynet), key=len, reverse=True)
        largest_comp = mynet.subgraph(comp_sorted_bysize[0])
        #print("Warning: Your network is not connected. Returning the diameter of the largest connected component.")
        return(nx.diameter(largest_comp))

#############################################################
# THIS FUNCTION RETURNS THE SIZE OF THE LARGEST CONNECTED COMPONENT
def size_of_largest_connected_component(mynet):
    
        comp_sorted_bysize = sorted(nx.connected_components(mynet), key=len, reverse=True)
        
        return(len(comp_sorted_bysize[0]))
    
#############################################################
# THIS FUNCTION RETURNS THE LARGEST CONNECTED COMPONENT AS A NETWORK
def largest_connected_component(mynet):
    
        comp_sorted_bysize = sorted(nx.connected_components(mynet), key=len, reverse=True)
        largest_comp = mynet.subgraph(comp_sorted_bysize[0])
        
        return(largest_comp)

#############################################################
# THIS FUNCTION RETURNS a DICTIONARY FOR THE COMMUNITY PARTITION
#  KEYS: MODULE ID, VALS: LIST OF NODE IDS IN THAT MODULE
def get_partition_dict(community_list):

    part = {}
    mod_id = 0
    for nodelist in community_list:
        part[mod_id] = nodelist
        mod_id = mod_id + 1

    return part

#######################################
# THIS FUNCTION CALCULATES THE MAXIMUM POSSIBLE MODULARITY IN A NETWORK
def calculate_Qmax(G, mod_nodes):

    Lt= sum([G.degree(node) for node in G.nodes()])
    total  =0

    for mod in mod_nodes.keys():
        Lk = sum([G.degree(node) for node in mod_nodes[mod]])
        total+= (1.0*Lk/Lt) - (1.0*Lk/Lt)**2 


    return total

#############################################################
# THIS FUNCTION RETURNS THE MODULARITY OF THE NETWORK (code from Networkx 2.4cr)
def relative_modularity(G, community_list):
# Computes Q value of a network when the modules are known (community_list is a list of lists with node ids)
# The returned value is Qrel = Q/Qmax

    mod_nodes = get_partition_dict(community_list)
    mods = len(mod_nodes.keys()) # number of modules
    s = [len(mod_nodes[x]) for x in range(0,mods)]
    nodes, degrees = zip(*G.degree()) # nodes, degree
    avg_deg = np.mean(degrees)
    N = len(G.nodes())
    Q = 0
    wd_bar = []
    d_bar = []
    for modules in range (0,mods):
        wdsum = 0
        dsum = 0
        wdsum = []
        dsum = []
        for node in mod_nodes[modules]:
            aii = [n for n in G.neighbors(node)]# total degree of a node
            a_set = set(aii) # set of all the neighbors
            mod_set = set(mod_nodes[modules]) # set of nodes in nodal module
            eii = list(a_set.intersection(mod_set)) #set of neighbors present in the same module
            wdsum.append(len(eii))
            dsum.append(len(aii))

        wd_bar.append(np.mean(wdsum))
        d_bar.append(np.mean(dsum))

    Q_list = [((wd_bar[i]*s[i])/(1.0*avg_deg*N)) - (s[i]/(1.0*N))**2 for i in range(0,mods)]
    Q = sum(Q_list)
    Qmax = calculate_Qmax(G, mod_nodes)

    return Q/float(Qmax)

#############################################################
# THIS FUNCTION CONVERTS THE OUTPUT OF THE COMMUNITY STRUCTURE ALGORITHM
#  INTO A MORE USEABLE FORMAT
def make_partition_into_list(communitylist,G):
# Returns a list of community ids for all nodes in the network
#  communitylist is a list of lists that contains node ids by community
#  G is a network

    # create a dictionary for the partition first (need to do this to ensure node order is correct)
    cnt = 0
    partition = {}
    for cc in communitylist:
        for node in cc:
            partition[node] = cnt
        cnt = cnt + 1

    # Now, create a list of community ids only (in the order that nodes are in G.nodes())
    comm_list = []
    for node in G.nodes():
        comm_list.append(partition[node])

    return comm_list


#############################################################
# THIS FUNCTION IMPLEMENTS THE PERCOLATION MODEL ONCE ON A NETWORK
def percolation_on_network(G,T):
# This function implements a percolation simulation on a contact 
#  network, Network, with transmissibility, T.
    Network = G.copy()
    # Initialize variables for the list of infected and recovered individuals
    infected = []                        
    recovered = []
    infected_count = 0
        
    ##################
    # Choose one node to infect (patient zero) so that outbreak can be seeded
    p_zero = rnd.choice(list(Network.nodes())) # Randomly choose one node from the network
    infected = [p_zero]                  # The node p_zero is now infected
    infected_count = 1

    ##################
    # Run the percolation simulation to simulate disease spread in network
    while infected:                      #Continue this process while there are any indivdiuals in the infected list
    
        infector = infected[0]           # pick out the first individual in the infected list

        ##################
        for neigh in list(Network.neighbors(infector)): # for all the nodes connected to (i.e. neighbors of) the infector 

            if neigh not in infected and neigh not in recovered: # check if this neighbor is susceptible

                # figure out if infector is successful at infecting neighbor "neigh"
                if rnd.random() < T:                     # if infector does infect neigh
                    infected.append(neigh)               # add neigh to the list of infected nodes (so it can infect others)
                    infected_count = infected_count +1   # add  one to the infected count

        # since infector has now had a chance to infected all its neighbors,
        #  we can remove it from the infected list, and put it in the recovered list
        infected.remove(infector)
        recovered.append(infector)
    
    # return the number of individuals (nodes) infected in this outbreak
    return infected_count


#############################################################
# THIS FUNCTION CARRIES OUT MONTE CARLO PERCOLATION MODEL SIMULATIONS
def percolation_results(G, T):
# This function carries out Monte Carlo simulations with the percolation model
#  Input: G = host population contact network, T = pathogen transmissibility
#  Output: average large epidemic size, average small outbreak size

    Network = G.copy()
    
    ##################
    # initialize lists for small outbreak and large epidemic sizes
    large_epidemic = []
    small_outbreak = []
    # initialize counter for how many large epidemics there have been
    large_epi_count = 0
    
    ##################
    # define parameters for the Monte Carlo simulation
    num_simulations = 250
    largeepi_threshold = 0.05
    population_size = nx.number_of_nodes(Network)
    
    ##################
    # Run the Monte Carlo simulation
    for sim in range(0,num_simulations):
        
        # Do one simulation of the percolation model
        infected_count= percolation_on_network(Network,T)

        # Decide if it is a small or large epidemic based on the epidemic threshold
        if infected_count > largeepi_threshold*population_size:  
            # if yes, save the infected count in the large_epidemic list
            large_epidemic.append(infected_count)
            # and also, increase the counter of how many large epidemics have occurred
            large_epi_count = large_epi_count + 1
        else: 
            # if no, save the infected count in the small_outbreak list
            small_outbreak.append(infected_count)
    
    # calculate the average size of small outbreak and large epidemics 
    average_large_epi_size= np.mean(large_epidemic)
    average_small_out_size= np.mean(small_outbreak)
    
    # calculate the probability of an epidemic
    prob_epidemic = 1.0*large_epi_count/num_simulations
    
    # return the average size of large epidemics and small outbreaks
    return average_large_epi_size, average_small_out_size
