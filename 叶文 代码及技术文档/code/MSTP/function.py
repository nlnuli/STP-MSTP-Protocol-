import networkx as nx
##选择出现重复连接的对应switch，为选拔backup端口准备
def judge_from_the_same_switch(list1):
    #1 表示不重复 0表示重复
    list2 = list1[:]
    n = len(list1)
    for i in range(n):
        list2[i] = list2[i][0:4]
    list2 = list(set(list2))
    n1 = len(list2)
    if n1 == n :
        return 1
    else:
        return 0

#哈希计数，选拔对应的重复列表
def count_num(list1):
    list2 = list1[:]
    n = len(list1)
    for i in range(n):
        list2[i] = list2[i][0:4]
    dict1 = dict()

    for item in list2:
        if item in dict1:  # 直接判断key在不在字典中
            dict1[item] += 1
        else:
            dict1[item] = 1
    list2 = list()
    for i in dict1:
        if dict1[i] >1:
            for j in list1:
                if i in j:
                    list2.append(j)
    return list2

#选招对应switch_name的BID
def find_bid(switch_name, switch_list):
    for switch in switch_list:
        if switch.switch_name == switch_name:
            return switch.bid

##目前可以找到每一个域内对应switch的bid 和 域的名字
def find_name(switch_bid, switch_list):
    for switch in switch_list:
        if switch.bid == switch_bid:
            return switch.switch_name

# 根据dijist算法计算最短路径长度
def rpc(node1, node2,g):
    #断开对应的端口计算
    p = nx.shortest_path_length(g,source = node1, target = node2, weight = 'cost' )
    return p

# 根据dijist算法计算最短路径
def path(node1,node2,g):
    p = nx.shortest_path(g, source = node1, target = node2, weight = 'cost')
    return p

# 根据switch_name寻找对应switch
def find_switch(switch_name,switch_list):
    for switch in switch_list:
        if switch.switch_name == switch_name:
            return switch

#根据port_name寻找bid
def find_designated_bridge(Designated_port_name,switch_list):
    for switch in switch_list:
        port_list = switch.port
        for port in port_list:
            name = switch.switch_name + '-' + str(port)
            if name == Designated_port_name:
                print(switch.bid)
                return switch.bid
#寻找DP对应pid
def find_designated_pid(Designated_port_name,g):
    for node in g.nodes(data = True):
        if node[0] == Designated_port_name:
            return node[1]['PID']

#寻找自身对应PID
def find_self_pid(name,g):
    for node in g.nodes(data = True):
        if node[0] == name:
            return node[1]['PID']

#恢复对应edge(选拔backup删除）
def recover_backup_edge(backup_del,g):
    for i in backup_del:
        g.add_edge(i[0], i[1], cost = i[2]['cost'], VLAN = i[2]['VLAN'], region_name = i[2]['region_name'])

#恢复对应node(选拔backup删除）
def recover_backup_node(backup,g):
    for port_data in backup:
        g.add_node(port_data[0], PID=port_data[1]['PID'], Root_bridge_ID=port_data[1]['Root_bridge_ID'], ERPC=0, \
                   Region_bridge_ID=port_data[1]['Region_bridge_ID'], IRPC=0, Designated_BID=-1, Designated_PID=-1, received_PID=-1, Port_status=port_data[1]['Port_status'],\
                   switch_bid=port_data[1]['switch_bid'], portID=port_data[1]['portID'], Port_priority=port_data[1]['Port_priority'])
        g.nodes[port_data[0]]['Region_bridge_ID'] = g.nodes[ port_data[0][0:4] ]['Region_bridge_ID']