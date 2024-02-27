import pandas as pd
import time
import networkx as nx
import matplotlib.pyplot as plt
import PIL

g = nx.Graph()  # 创建无相图

##节点添加
print("-------添加节点中--------")


# 定义switch
class Switch:
    # port端口，name，mac，priority，bid
    def __init__(self, port_list, mac, switch_name, priority, region_name):
        self.port = []
        self.switch_name = switch_name
        for i in port_list:
            self.port.append(i)
        self.mac = mac  ## switch bid
        self.priority = priority
        self.bid = int(str(self.priority) + str(self.mac))  # bid 代表优先级
        self.region_name = region_name


file_path = '/Users/yewen/Desktop/2023毕业设计/code/data for mstp.xlsx'
raw_data = pd.read_excel(file_path, header=0, sheet_name='switch')
data = raw_data.values

##添加switch 信息
# 初始化switch 信息
switch_list = list()
print('-----switch信息添加----')
for i in range(data.shape[0]):
    ## 每行data
    switch_data = data[i]
    str1 = str(switch_data[0])
    list1 = str1.split(',')
    list1 = [int(i) for i in list1]
    print(list1)
    switch_list.append(Switch(list1, switch_data[2], switch_data[3], switch_data[1], switch_data[4]))

print('--------switch 添加完毕--------')

print('--------添加端口port信息--------')
raw_data = pd.read_excel(file_path, header=0, sheet_name='port')
data = raw_data.values
for i in range(data.shape[0]):
    port_data = data[i]
    pid = int(str(port_data[2]) + str(port_data[1]))
    g.add_node(port_data[0], PID=pid, Root_bridge_ID='0', ERPC=0, \
               Region_bridge_ID=0, IRPC=0, Designated_BID=0, Designated_PID=0, received_PID=0, Port_status='None',
               switch_bid=-1, portID=port_data[1], Port_priority=port_data[2], )
##对port 的switch进行维修
for switch in switch_list:
    name = switch.switch_name
    for port in switch.port:
        g.nodes[name + '-' + str(port)]['switch_bid'] = switch.bid
        g.nodes[name + '-' + str(port)]['Root_bridge_ID'] = switch.bid
        g.nodes[name + '-' + str(port)]['Region_bridge_ID'] = switch.bid

    g.add_node(switch.switch_name, PID=-1, Root_bridge_ID=switch.bid, ERPC=-1, \
               Region_bridge_ID=switch.bid, IRPC=-1, Designated_BID=-1, Designated_PID=-1, received_PID=-1,
               Port_status='switch', switch_bid=switch.bid, portID=-1, Port_priority=-1)

for node in g.nodes(data=True):
    print(node)
print('------node 信息添加完毕--------')
print('------添加edge信息------------')
raw_data = pd.read_excel(file_path, header=0, sheet_name='edge')
data = raw_data.values
for i in range(data.shape[0]):
    data_edge = list(data[i])
    g.add_edge(data_edge[0], data_edge[1], cost=data_edge[2], VLAN=data_edge[3], region_name=data_edge[4])

print('--------创建edge region 映射关系------')
switch_region = {}
for switch in switch_list:
    switch_region[switch.switch_name] = switch.region_name
for edge in g.edges.data():
    str1 = (edge[0][0:4])
    str2 = (edge[1][0:4])
    if switch_region[str1] == switch_region[str2]:
        g[edge[0]][edge[1]]['region_name'] = switch_region[edge[1][0:4]]
    else:
        g[edge[0]][edge[1]]['region_name'] = 'mid_region'

for switch in switch_list:
    # 根据路由器来添加节点
    port_list = switch.port
    switchname = switch.switch_name
    for port in port_list:
        g.add_edge(switchname + '-' + str(port) \
                   , switchname, \
                   cost=0, VLAN=-1, region_name=switch.region_name)

for edge in g.edges(data=True):
    print(edge)
print('------edge添加完毕-------')

## ---------现在开始加载端口的设置
print('------开始选举总根')
root_bridge = switch_list[0].bid
root_bridge_name = switch_list[0].switch_name
for switch in switch_list:
    if root_bridge > switch.bid:
        root_bridge = switch.bid
        root_bridge_name = switch.switch_name
##选举出最小的bid
print("全局根桥为{}".format(root_bridge_name))
##更新端口信息
for node in g.nodes(data=True):
    ##更新Root_bridhe_ID:
    g.nodes[node[0]]['Root_bridge_ID'] = root_bridge

print('--------选举备份端口Backup------')


##创建端口映射关系
def judge_from_the_same_switch(list1):
    # 1 表示不重复 0表示重复
    list2 = list1[:]
    n = len(list1)
    for i in range(n):
        list2[i] = list2[i][0:4]
    list2 = list(set(list2))
    n1 = len(list2)
    if n1 == n:
        return 1
    else:
        return 0


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
        if dict1[i] > 1:
            for j in list1:
                if i in j:
                    list2.append(j)
    return list2


port_edge = dict()
for edge in g.edges(data=True):
    key = edge[0]
    port_edge.setdefault(key, []).append(edge[1])
    key = edge[1]
    port_edge.setdefault(key, []).append(edge[0])

print(port_edge)
# 逐个访问 字典，判断有无来自两个的
backup_del = list()
backup = []
backup_name = []
for key in port_edge:
    list1 = port_edge[key]
    # key 为汇聚的东西
    if len(key) <= 4:
        continue
    if (judge_from_the_same_switch(list1) == 1):
        continue
    if (judge_from_the_same_switch(list1) == 0):
        # 重复了 堵塞其中一个为backup list1中存在重复的端口
        # 挨个检查对应的
        repeat = count_num(list1)
        print(repeat)
        print(key)
        # 选择一个进行阻塞
        max_cost = -1
        max1 = repeat[0]
        for i in repeat:
            if max_cost < g[key][i]['cost']:
                max_cost = g[key][i]['cost']
                max1 = i
        print('-----{}-{}由于重复阻塞成为backup-----'.format(key, max1))
        g.nodes[max1]['Port_status'] = 'backup'
        print(g[max1][key])
        backup_del.append([max1, key, g[max1][key]])
        backup.append([max1, g.nodes[max1]])
        backup_name.append(max1)
        print(g.nodes[max1])
        g.remove_edge(key, max1)
        g.remove_node(max1)

print("backup删除链路为：", backup_del)
print("backup删除节点为", backup)

for node in g.nodes(data=True):
    print(node[0], node[1]['Port_status'])

##去掉backup来计算其他的节点

for node in g.nodes(data=True):
    print(node)

##更新Root_bridgr_ID成功
##分别为每个域分开计算
## region:
print('域映射关系')

region_dict = {}
for switch in switch_list:
    key = switch.region_name
    region_dict.setdefault(key, []).append(switch.switch_name)
print(region_dict)


def find_bid(switch_name):
    for switch in switch_list:
        if switch.switch_name == switch_name:
            return switch.bid


def find_name(switch_bid):
    for switch in switch_list:
        if switch.bid == switch_bid:
            return switch.switch_name


print("-----开始生成IST------")
##对每个域分开生成


##断开edge
edge_list = []
for edge in g.edges(data=True):
    print(list(edge))
    if edge[2]['region_name'] == 'mid_region':
        edge = list(edge)
        print(edge)
        edge_list.append(list(edge))
print("------已经选拔出域间edge并且存放在edge_list 中-------")
print(edge_list)
##断开edge
for i in range(len(edge_list)):
    g.remove_edge(edge_list[i][0], edge_list[i][1])
print("-----------域间edge删除成功----------------")

for edge in g.edges(data=True):
    print(edge)

print('-------选拔域边缘端口 domain_edge--------')
domain_edge_list = list()
for edge in edge_list:
    domain_edge_list.append(edge[0])
    domain_edge_list.append(edge[1])
print(domain_edge_list)
domain_edge_list = list(set(domain_edge_list))
for node in g.nodes(data=True):
    if node[0] in domain_edge_list and g.nodes[node[0]]['Port_status'] != 'backup':
        g.nodes[node[0]]['Port_status'] = 'domain_edge_port'

for node in g.nodes(data=True):
    print(node[0], node[1]['Port_status'])

print('-------域边缘端口选举完毕-------')


def rpc(node1, node2):
    # 断开对应的端口计算
    p = nx.shortest_path_length(g, source=node1, target=node2, weight='cost')
    return p


def path(node1, node2):
    p = nx.shortest_path(g, source=node1, target=node2, weight='cost')
    return p


def find_switch(switch_name):
    for switch in switch_list:
        if switch.switch_name == switch_name:
            return switch


def find_designated_bridge(Designated_port_name):
    for switch in switch_list:
        port_list = switch.port
        for port in port_list:
            name = switch.switch_name + '-' + str(port)
            if name == Designated_port_name:
                print(switch.bid)
                return switch.bid


def find_designated_pid(Designated_port_name):
    for node in g.nodes(data=True):
        if node[0] == Designated_port_name:
            return node[1]['PID']


def find_self_pid(name):
    for node in g.nodes(data=True):
        if node[0] == name:
            return node[1]['PID']


print("--------开始在域内选举MSTI--------")

print("---------域根桥选举-----------")
for region in region_dict:
    switch_region_list = region_dict[region]
    print(region, switch_region_list)
    ##bid
    ##对域分开操作
    ##寻找region root
    switch_bid = list()
    for switch_name in switch_region_list:
        switch_bid.append(find_bid(switch_name))
    region_root_bid = min(switch_bid)
    ##目前可以找到每一个域内对应switch的bid 和 域的名字
    region_root_name = find_name(region_root_bid)
    print("{}域根桥bid为{},名字为{}".format(region, region_root_bid, region_root_name))
    print('-------{}域根桥选举完毕'.format(region) + '----------')
    ##更新每一个域node节点的
    ##更新
    ##已断开e域间edge
    ##now 我们断开域内的edge

    del_switch = list()
    for switch in switch_list:
        if switch.bid not in switch_bid:
            continue
        if switch.bid in switch_bid:
            del_switch.append(switch)

    ## del_switch存储着域的switch

    for node in g.nodes(data=True):
        if node[1]['switch_bid'] in switch_bid:
            g.nodes[node[0]]['Region_bridge_ID'] = region_root_bid
        if node[1]['switch_bid'] == region_root_bid and node[1]['Port_status'] != 'switch' and node[1][
            'Port_status'] != 'domain_edge_port':
            g.nodes[node[0]]['Port_status'] = 'DP'
    print("{}域内node，BPDU中Region_bridge_ID已更新".format(region))

    print("------开始更新IRPC 为了选举域内根端口-------")
    region_switch_list = list()  # 域中对应的switch
    for switch_name in switch_region_list:
        region_switch_list.append(find_switch(switch_name))
    for switch in region_switch_list:
        # 依次对每个switch进行更新
        if switch.bid == region_root_bid:
            target_switch = switch  ##域内根桥
            # target port 更逊
            for port in target_switch.port:
                g.nodes[switch.switch_name + '-' + str(port)]['Designated_BID'] = switch.bid
                g.nodes[switch.switch_name + '-' + str(port)]['Designated_PID'] = \
                g.nodes[switch.switch_name + '-' + str(port)]['PID']

            continue
        port_list = switch.port  # 域内桥上的port
        for port in port_list:
            if switch.switch_name + '-' + str(port) not in backup_name:
                g.remove_edge(switch.switch_name, switch.switch_name + '-' + str(port))
            ##已经删除了switch对应的节点
        ## domain_edge_list 为域边缘的端口
        # 域边缘端口不参与计算，不用管
        # 此switch 对应switch-port edge已经删除
        ##对应交换机
        for port in port_list:

            port_name = switch.switch_name + '-' + str(port)
            if switch.switch_name + '-' + str(port) in backup_name:
                continue
            if port_name in domain_edge_list:
                continue
            ##此时不为边缘端口需要进行计算
            min_num = 9999999
            Designated_port_name = str()
            for j in target_switch.port:
                port_name2 = target_switch.switch_name + '-' + str(j)
                p1 = rpc(port_name, port_name2)
                if min_num > p1:
                    min_num = p1
                    print('{}{}为{}'.format(port_name, port_name2, min_num))
                    # 更优秀
                    short_path = path(port_name, port_name2)
                    Designated_port_name = short_path[1]

            ##此时我们需要进行更新BPDU
            g.nodes[port_name]['IRPC'] = min_num
            g.nodes[port_name]['Designated_BID'] = find_designated_bridge(Designated_port_name)
            g.nodes[port_name]['Designated_PID'] = find_designated_pid(Designated_port_name)
            g.nodes[port_name]['received_PID'] = find_self_pid(port_name)

        for port in port_list:
            if switch.switch_name + '-' + str(port) in backup_name:
                continue
            g.add_edge(switch.switch_name, switch.switch_name + '-' + str(port), cost=0, VLAN=-1,
                       region_name=switch.region_name)
            print('add {} {}'.format(switch.switch_name, switch.switch_name + '-' + str(port)))
    print('--------域BPDU更新完毕--------开始选举根节点')
    # region_switch_list 域内switch列表 域内选举
    for switch in region_switch_list:
        # 每个switch均有
        if switch.bid == region_root_bid:
            target_switch = switch  ##域内根桥
            continue
        ##开始选举
        rootport = switch.switch_name + '-' + str(switch.port[0])
        for i in switch.port:
            port_name = switch.switch_name + '-' + str(i)
            if port_name in backup_name:
                continue
            if port_name in domain_edge_list:
                continue
            if g.nodes[port_name]['IRPC'] < g.nodes[rootport]['IRPC']:
                rootport = port_name
            elif g.nodes[port_name]['IRPC'] > g.nodes[rootport]['IRPC']:
                pass
            elif g.nodes[port_name]['IRPC'] == g.nodes[rootport]['IRPC']:
                if g.nodes[port_name]['Designated_BID'] < g.nodes[rootport]['Designated_BID']:
                    rootport = port_name
                elif g.nodes[port_name]['Designated_BID'] == g.nodes[rootport]['Designated_BID']:
                    if g.nodes[port_name]['Designated_PID'] < g.nodes[rootport]['Designated_PID']:
                        rootport = port_name
                    elif g.nodes[port_name]['Designated_PID'] == g.nodes[rootport]['Designated_PID']:
                        if g.nodes[port_name]['received_PID'] < g.nodes[rootport]['received_PID']:
                            rootport = port_name

        g.nodes[rootport]['Port_status'] = 'Root Port'
        ##选举指定端口
    print("--------域内ROOT PORT选拔完毕---------")
    for node in g.nodes(data=True):
        print(node)
    print("-------根据选拔跟端口信息进行更新配置BPDU信息选拔DP-------")
    for switch in region_switch_list:
        if switch.bid == region_root_bid:
            target_switch = switch  ##域内根桥
            continue
        ##开始选举DP端口
        ##switch 不是域根
        port_list = switch.port
        min_cost = 999999
        for port in port_list:
            port_name = switch.switch_name + '-' + str(port)
            if switch.switch_name + '-' + str(port) in backup_name:
                continue
            if g.nodes[port_name]['Port_status'] == 'domain_edge_port':
                # 域间的不进行更新
                continue
            if min_cost > g.nodes[port_name]['IRPC']:
                min_cost = g.nodes[port_name]['IRPC']
        # 更新出switch中最小的
        for port in port_list:
            if switch.switch_name + '-' + str(port) in backup_name:
                continue
            port_name = switch.switch_name + '-' + str(port)
            if g.nodes[port_name]['Port_status'] == 'domain_edge_port':
                # 域间的不进行更新
                continue
            g.nodes[port_name]['IRPC'] = min_cost
            g.nodes[port_name]['Designated_BID'] = switch.bid
            g.nodes[port_name]['Designated_PID'] = g.nodes[port_name]['PID']

    for node in g.nodes(data=True):
        print(node)
    ## 对于每个edge选拔出一个指定端口
    DP_list = list()
    for port in target_switch.port:
        portName = target_switch.switch_name + '-' + str(port)
        if g.nodes[portName]['Port_status'] == 'domain_edge_port':
            # 不更新
            continue
        DP_list.append(portName)
    # DP_list存储着域内为DP的端口

    for edge in g.edges(data=True):
        if (edge[2]['cost'] == 0):
            continue
        print(edge)

    for edge in g.edges(data=True):
        if edge[0] in DP_list or edge[1] in DP_list or edge[2]['cost'] == 0:
            # 指定端口已经选举
            continue
        if g.nodes[edge[0]]['IRPC'] < g.nodes[edge[1]]['IRPC']:
            g.nodes[edge[0]]['Port_status'] = 'DP'
        elif g.nodes[edge[0]]['IRPC'] > g.nodes[edge[1]]['IRPC']:
            g.nodes[edge[1]]['Port_status'] = 'DP'
        elif g.nodes[edge[0]]['IRPC'] == g.nodes[edge[1]]['IRPC']:
            if g.nodes[edge[0]]['Designated_BID'] < g.nodes[edge[1]]['Designated_BID']:
                g.nodes[edge[0]]['Port_status'] = 'DP'
            elif g.nodes[edge[0]]['Designated_BID'] > g.nodes[edge[1]]['Designated_BID']:
                g.nodes[edge[1]]['Port_status'] = 'DP'
            else:
                if g.nodes[edge[0]]['Designated_PID'] < g.nodes[edge[1]]['Designated_PID']:
                    g.nodes[edge[0]]['Port_status'] = 'DP'
                elif g.nodes[edge[0]]['Designated_PID'] > g.nodes[edge[1]]['Designated_PID']:
                    g.nodes[edge[1]]['Port_status'] = 'DP'
    print("--------DP端口选择完毕--------")
    region_port = list()
    for switch in region_switch_list:
        for port in switch.port:
            portName = switch.switch_name + '-' + str(port)
            region_port.append((portName))
    print(region_port)
    for edge in g.edges(data=True):

        if edge[0] in region_port and edge[1] in region_port and edge[2]['cost'] != 0:
            print(edge)
            if g.nodes[edge[0]]['Port_status'] == 'None':
                g.nodes[edge[0]]['Port_status'] = 'AP'
            if g.nodes[edge[1]]['Port_status'] == 'None':
                g.nodes[edge[1]]['Port_status'] = 'AP'

    print("--------AP端口选择完毕--------")


##恢
def recover_backup_edge(backup_del):
    for i in backup_del:
        print(list1)
        g.add_edge(i[0], i[1], cost=i[2]['cost'], VLAN=i[2]['VLAN'], region_name=i[2]['region_name'])


def recover_backup_node(backup):
    for port_data in backup:
        g.add_node(port_data[0], PID=port_data[1]['PID'], Root_bridge_ID=port_data[1]['Root_bridge_ID'], ERPC=0, \
                   Region_bridge_ID=port_data[1]['Region_bridge_ID'], IRPC=0, Designated_BID=-1, Designated_PID=-1,
                   received_PID=-1, Port_status=port_data[1]['Port_status'], \
                   switch_bid=port_data[1]['switch_bid'], portID=port_data[1]['portID'],
                   Port_priority=port_data[1]['Port_priority'])
        g.nodes[port_data[0]]['Region_bridge_ID'] = g.nodes[port_data[0][0:4]]['Region_bridge_ID']


recover_backup_edge(backup_del)
recover_backup_node(backup)

for node in g.nodes(data=True):
    print(node)

for node in g.nodes(data=True):
    print(node[0], node[1]['Port_status'])

    ##开始选拔域间DP端口，针对的是每个线路
    # 需要重新计算RPC
    ## 根据跟端口的信息来进行替换为自己的ID

    # for node in g.nodes(data=True):
    #   print(node)

    ####### code section

    """

    for edge in g.edges(data=True):
        print(edge)
    """

"""
##添加edge
for edge in edge_list:
    g.add_edges_from([ (edge[0],edge[1],edge[2]) ])

for edge in g.edges(data=True):
     print(edge)
"""

##添加域间路由
