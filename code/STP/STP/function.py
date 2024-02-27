import networkx as nx



#根据djstr算法计算最短路径的长度
def rpc(node1, node2,g):
    #断开对应的端口计算
    p = nx.shortest_path_length(g,source = node1, target = node2, weight = 'weight' )
    return p

#根据djstr算法计算最短路径
def path(node1,node2,g):
    p = nx.shortest_path(g, source = node1, target = node2, weight = 'weight')
    return p

#根据端口名寻找switch bid
def find_bid(port1, switch_list): #参数为端口
    for switch in switch_list:
        if port1 in switch.port:
            return switch.number