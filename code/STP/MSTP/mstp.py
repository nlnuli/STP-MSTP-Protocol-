import pandas as pd
import networkx as nx
import time
import matplotlib.pyplot as plt
import PIL
start = time.time()
g = nx.Graph()  # 创建无相图
fp = open('/Users/yewen/Desktop/2023毕业设计/code/STP/data_test/print.txt',"w")
fp2 = open('/Users/yewen/Desktop/2023毕业设计/code/STP/data_test/role.txt', "w")
##节点添加
print("-------添加节点中--------", file = fp)


# 定义switch类
class Switch:
    #内容： port端口，name，mac，priority，bid
    def __init__(self, port_list, mac, switch_name, priority, region_name, mac_list):
        self.port = []
        self.switch_name = switch_name
        for i in port_list:
            self.port.append(i)
        self.mac = mac  ## switch bid
        self.priority = priority
        self.bid = int(str(self.priority) + str(self.mac))  # bid 代表优先级
        self.region_name = region_name
        self.mac_list = mac_list

class fwd_table:
    def __init__(self, switch_name):
        self.name = switch_name
        self.fwd_index = list()

file_path = '/Users/yewen/Desktop/2023毕业设计/code/STP/data_test/mstp.xls'
raw_data = pd.read_excel(file_path, header=0, sheet_name='switch')
data = raw_data.values

##添加switch 信息
# 初始化switch 信息
switch_list = list()
print('-----switch信息添加----', file = fp)
print(" ")
for i in range(data.shape[0]):
    ## 每行数据
    switch_data = data[i]
    print(switch_data)
    str1 = str(switch_data[0])
    list1 = str1.split(',')
    list1 = [int(i) for i in list1]
    print(list1, file = fp)


    switch_list.append(Switch(list1, switch_data[2], switch_data[3], switch_data[1], switch_data[4],switch_data[5]))

print('--------switch 添加完毕--------', file = fp)

print('--------添加端口port信息--------', file = fp)
raw_data = pd.read_excel(file_path, header=0, sheet_name='port')
data = raw_data.values
for i in range(data.shape[0]):
    port_data = data[i]
    print(port_data, file = fp)
    pid = int(str(port_data[2]) + str(port_data[1]))
    g.add_node(port_data[0], PID=pid, Root_bridge_ID='0', ERPC=0, \
               Region_bridge_ID=0, IRPC=0, Designated_BID=0, Designated_PID=0, received_PID=0, Port_status='None',
               switch_bid=-1, portID=port_data[1], Port_priority=port_data[2],VLAN = port_data[3] )
##对端口对应 的switch进行数据维修
for switch in switch_list:
    name = switch.switch_name
    for port in switch.port:
        g.nodes[name + '-' + str(port)]['switch_bid'] = switch.bid
        g.nodes[name + '-' + str(port)]['Root_bridge_ID'] = switch.bid
        g.nodes[name + '-' + str(port)]['Region_bridge_ID'] = switch.bid

    g.add_node(switch.switch_name, PID=-1, Root_bridge_ID=switch.bid, ERPC=-1, \
               Region_bridge_ID=switch.bid, IRPC=-1, Designated_BID=-1, Designated_PID=-1, received_PID=-1,
               Port_status='switch', switch_bid=switch.bid, portID=-1, Port_priority=-1, VLAN = 'none')

for node in g.nodes(data=True):
    print(node, file = fp)
print('------node 信息添加完毕--------', file = fp)
print('------添加edge信息------------', file = fp)
raw_data = pd.read_excel(file_path, header=0, sheet_name='edge')
data = raw_data.values
for i in range(data.shape[0]):
    data_edge = list(data[i])
    g.add_edge(data_edge[0], data_edge[1], cost=data_edge[2], region_name='none')

print('--------创建edge region 映射关系------', file = fp)
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
                   cost=0, region_name=switch.region_name)

for edge in g.edges(data=True):
    print(edge, file = fp)
print('------edge添加完毕-------', file = fp)

## ---------现在开始加载端口的设置
print('------开始选举总根', file = fp)
root_bridge = switch_list[0].bid
root_bridge_name = switch_list[0].switch_name
for switch in switch_list:
    if root_bridge > switch.bid:
        root_bridge = switch.bid
        root_bridge_name = switch.switch_name
##选举出最小的bid
print("全局根桥为{}".format(root_bridge_name), file = fp)
##更新端口信息
for node in g.nodes(data=True):
    ##更新Root_bridhe_ID:
    g.nodes[node[0]]['Root_bridge_ID'] = root_bridge

print('--------选举备份端口Backup------', file = fp)


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

print(port_edge, file = fp)
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
        print(repeat, file = fp)
        print(key, file = fp)
        # 选择一个进行阻塞
        max_cost = -1
        max1 = repeat[0]
        for i in repeat:
            if max_cost < g[key][i]['cost']:
                max_cost = g[key][i]['cost']
                max1 = i
        print('-----{}-{}由于重复阻塞成为backup-----'.format(key, max1), file = fp)
        g.nodes[max1]['Port_status'] = 'backup'
        print(g[max1][key], file = fp)
        backup_del.append([max1, key, g[max1][key]])
        backup.append([max1, g.nodes[max1]])
        backup_name.append(max1)
        print(g.nodes[max1], file = fp)
        g.remove_edge(key, max1)
        g.remove_node(max1)

print("backup删除链路为：", backup_del, file = fp)
print("backup删除节点为", backup, file = fp)

for node in g.nodes(data=True):
    print(node[0], node[1]['Port_status'], file = fp)

##去掉backup来计算其他的节点

for node in g.nodes(data=True):
    print(node, file = fp)

##更新Root_bridgr_ID成功
##分别为每个域分开计算
## region:
print('----------域映射关系---------', file = fp)

region_dict = {}
for switch in switch_list:
    key = switch.region_name
    region_dict.setdefault(key, []).append(switch.switch_name)
print(region_dict, file = fp)


def find_bid(switch_name):
    for switch in switch_list:
        if switch.switch_name == switch_name:
            return switch.bid


def find_name(switch_bid):
    for switch in switch_list:
        if switch.bid == switch_bid:
            return switch.switch_name


print("-----开始生成IST------", file = fp)
##对每个域分开生成


##断开edge
edge_list = []
for edge in g.edges(data=True):
    print(list(edge), file = fp)
    if edge[2]['region_name'] == 'mid_region':
        edge = list(edge)
        print(edge)
        edge_list.append(list(edge))
print("------已经选拔出域间edge并且存放在edge_list 中-------", file = fp)
print(edge_list, file = fp)
##断开edge
for i in range(len(edge_list)):
    g.remove_edge(edge_list[i][0], edge_list[i][1])
print("-----------域间edge删除成功----------------", file = fp)

for edge in g.edges(data=True):
    print(edge, file = fp)

print('-------选拔域边缘端口 domain_edge--------', file = fp)
domain_edge_list = list()
for edge in edge_list:
    domain_edge_list.append(edge[0])
    domain_edge_list.append(edge[1])
print(domain_edge_list, file = fp)
domain_edge_list = list(set(domain_edge_list))
for node in g.nodes(data=True):
    if node[0] in domain_edge_list and g.nodes[node[0]]['Port_status'] != 'backup':
        g.nodes[node[0]]['Port_status'] = 'domain_edge_port'

for node in g.nodes(data=True):
    print(node[0], node[1]['Port_status'], file = fp)

print('-------域边缘端口选举完毕-------', file = fp)


def rpc(node1, node2,g):
    # 断开对应的端口计算
    p = nx.shortest_path_length(g, source=node1, target=node2, weight='cost')
    return p


def path(node1, node2,g):
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

                return switch.bid


def find_designated_pid(Designated_port_name):
    for node in g.nodes(data=True):
        if node[0] == Designated_port_name:
            return node[1]['PID']


def find_self_pid(name):
    for node in g.nodes(data=True):
        if node[0] == name:
            return node[1]['PID']


print("--------开始在域内选举MSTI--------", file = fp)

print("---------域根桥选举-----------", file = fp)
for region in region_dict:

    switch_region_list = region_dict[region]
    print(region, switch_region_list, file = fp)
    ##bid
    ##对域分开操作
    ##寻找region root
    switch_bid = list()
    for switch_name in switch_region_list:
        switch_bid.append(find_bid(switch_name))
    region_root_bid = min(switch_bid)
    ##目前可以找到每一个域内对应switch的bid 和 域的名字
    region_root_name = find_name(region_root_bid)
    print("{}域根桥bid为{},名字为{}".format(region, region_root_bid, region_root_name), file = fp)
    print('-------{}域根桥选举完毕'.format(region) + '----------', file = fp)
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
        if node[1]['switch_bid'] == region_root_bid and node[1]['Port_status'] != 'switch' and node[1]['Port_status'] != 'domain_edge_port':
            g.nodes[node[0]]['Port_status'] = 'DP'
    print("{}域内node，BPDU中Region_bridge_ID已更新".format(region), file = fp)

    print("------开始更新IRPC 为了选举域内根端口-------", file = fp)
    region_switch_list = list()  # 域中对应的switch
    for switch_name in switch_region_list:
        region_switch_list.append(find_switch(switch_name))
    target_switch = region_switch_list[0]
    for switch in region_switch_list:
        # 依次对每个switch进行更新
        if switch.bid == region_root_bid:
            target_switch = switch  ##域内根桥
            # target port 更逊
            for port in target_switch.port:
                g.nodes[switch.switch_name + '-' + str(port)]['Designated_BID'] = switch.bid
                g.nodes[switch.switch_name + '-' + str(port)]['Designated_PID'] = \
                g.nodes[switch.switch_name + '-' + str(port)]['PID']
            break

    for switch in region_switch_list:
        if switch.bid == region_root_bid:
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
        ##计算对应的rpc
        for port in port_list:

            port_name = switch.switch_name + '-' + str(port)
            if switch.switch_name + '-' + str(port) in backup_name:
                continue
            if port_name in domain_edge_list:
                continue
            ##此时不为边缘端口且不为备份端口需要进行计算
            min_num = 9999999
            Designated_port_name = str()
            for j in target_switch.port:
                port_name2 = target_switch.switch_name + '-' + str(j)
                p1 = rpc(port_name, port_name2,g)
                if min_num > p1:
                    min_num = p1
                    print('{}{}为{}'.format(port_name, port_name2, min_num), file = fp)
                    # 更优秀
                    short_path = path(port_name, port_name2,g)
                    Designated_port_name = short_path[1]

            ##此时我们需要进行更新BPDU
            g.nodes[port_name]['IRPC'] = min_num
            g.nodes[port_name]['Designated_BID'] = find_designated_bridge(Designated_port_name)
            g.nodes[port_name]['Designated_PID'] = find_designated_pid(Designated_port_name)
            g.nodes[port_name]['received_PID'] = find_self_pid(port_name)

        for port in port_list:
            if switch.switch_name + '-' + str(port) in backup_name:
                continue
            g.add_edge(switch.switch_name, switch.switch_name + '-' + str(port), cost=0,
                       region_name=switch.region_name)
            print('add {} {}'.format(switch.switch_name, switch.switch_name + '-' + str(port)), file = fp)
    print('--------域BPDU更新完毕--------开始选举根节点', file = fp)
    # region_switch_list 域内switch列表 域内选举
    for switch in region_switch_list:
        # 每个switch均有
        if switch.bid == region_root_bid:
            target_switch = switch  ##域内根桥
            continue
        ##开始选举
        rootport = ''
        for i in switch.port:
            port_name = switch.switch_name + '-' + str(i)
            if port_name in backup_name:
                continue
            if port_name in domain_edge_list:
                continue
            rootport= switch.switch_name + '-' + str(i)
            break

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
    print("--------域内ROOT PORT选拔完毕---------", file = fp)
    for node in g.nodes(data=True):
        print(node, file = fp)
    print("-------根据选拔跟端口信息进行更新配置BPDU信息选拔DP-------", file = fp)
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
        print(node, file = fp)
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
        print(edge, file = fp)

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
    print("--------DP端口选择完毕--------", file = fp)
    region_port = list()
    for switch in region_switch_list:
        for port in switch.port:
            portName = switch.switch_name + '-' + str(port)
            region_port.append((portName))
    print(region_port, file = fp)
    for edge in g.edges(data=True):

        if edge[0] in region_port and edge[1] in region_port and edge[2]['cost'] != 0:
            if g.nodes[edge[0]]['Port_status'] == 'None':
                g.nodes[edge[0]]['Port_status'] = 'AP'
            if g.nodes[edge[1]]['Port_status'] == 'None':
                g.nodes[edge[1]]['Port_status'] = 'AP'

    print("--------AP端口选择完毕--------", file = fp)


##恢
def recover_backup_edge(backup_del):
    for i in backup_del:
        print(list1, file = fp)
        g.add_edge(i[0], i[1], cost=i[2]['cost'], region_name=i[2]['region_name'])


def recover_backup_node(backup):
    for port_data in backup:
        g.add_node(port_data[0], PID=port_data[1]['PID'], Root_bridge_ID=port_data[1]['Root_bridge_ID'], ERPC=0, \
                   Region_bridge_ID=port_data[1]['Region_bridge_ID'], IRPC=0, Designated_BID=-1, Designated_PID=-1,
                   received_PID=-1, Port_status=port_data[1]['Port_status'], \
                   switch_bid=port_data[1]['switch_bid'], portID=port_data[1]['portID'],
                   Port_priority=port_data[1]['Port_priority'],VLAN = 'backup')
        g.nodes[port_data[0]]['Region_bridge_ID'] = g.nodes[port_data[0][0:4]]['Region_bridge_ID']

## 恢复 backup堵塞端口
recover_backup_edge(backup_del)
recover_backup_node(backup)
##恢复 域间线路 为后面的计算做好准备
for edge in edge_list:
    g.add_edges_from([ (edge[0],edge[1],edge[2]) ])
##

print("-------开始计算ERPC---------", file = fp)

for region in region_dict:
    switch_region_list = region_dict[region]
    print(region, switch_region_list, file = fp)

    switch_bid = list()
    for switch_name in switch_region_list:
        switch_bid.append(find_bid(switch_name))
    region_root_bid = min(switch_bid)
    ##目前可以找到每一个域内对应switch的bid 和 域的名字
    region_root_name = find_name(region_root_bid)
    region_switch = find_switch(region_root_name)                              #########后期需要进行函数修改
    print(region_switch.switch_name, file = fp)
    region_switch_list = list()
    for switch in switch_list:
        if switch.bid not in switch_bid:
            continue
        if switch.bid in switch_bid:
            region_switch_list.append(switch)

    root_bridge = find_switch(root_bridge_name)                               #########后期需要进行函数修改
    print(root_bridge.switch_name, file = fp)
    ##如果总根桥位于域中则为0
    if root_bridge == region_switch :
        for switch_name in switch_region_list:
            g.nodes[switch_name]['ERPC'] = 0
            switch = find_switch(switch_name)
            for port in switch.port:
                g.nodes[switch.switch_name + '-' + str(port)]['ERPC'] = 0
    else:
        ##计算ERPC
        target_port = root_bridge.switch_name + '-' + str(root_bridge.port[0])
        source_port = region_switch.switch_name + '-' + str(region_switch.port[0])
        r = rpc(target_port,source_port,g)
        for switch_name in switch_region_list:
            g.nodes[switch_name]['ERPC'] = r
            switch = find_switch(switch_name)
            for port in switch.port:
                g.nodes[switch.switch_name + '-' + str(port)]['ERPC'] = r

##目前ERPC生成完毕
print('----------开始选拔master端口-------------', file = fp)









for edge in g.edges(data = True):
    print(edge, file = fp)



for node in g.nodes(data=True):
    print(node, file = fp)

for node in g.nodes(data=True):
    print(node[0], node[1]['Port_status'], file = fp)
print('-----IST及 MSTI0 生成完毕---------', file = fp)
print("---------开始生成CST--------", file = fp)
#CIST 的计算只计算机只计算域间的cost不计算域内的cost edgeport 可能成为AP端口被堵塞
#master 端口位于域到总根最近的端口,每个域有一个

##将每个域看作一个switch 域间连接为switch连接
## EPRC为 域根到达总根的长度
G = nx.Graph()

for region in region_dict:
    switch_region_list = region_dict[region]
    print(region, switch_region_list, file = fp)

    switch_bid = list()
    for switch_name in switch_region_list:
        switch_bid.append(find_bid(switch_name))
    region_root_bid = min(switch_bid)
    ##目前可以找到每一个域内对应switch的bid 和 域的名字
    region_root_name = find_name(region_root_bid)



    region_switch_list = list()
    for switch in switch_list:
        if switch.bid not in switch_bid:
            continue
        if switch.bid in switch_bid:
            region_switch_list.append(switch)
    region_port = list()
    for switch in region_switch_list:
        for port in switch.port:
            if switch.switch_name + '-' + str(port) in backup_name:
                continue
            region_port.append(switch.switch_name + '-' + str(port))
    #查找其中对应的edge——port
    del_list = list()
    for port_name in region_port:
        if g.nodes[port_name]['Port_status'] != 'domain_edge_port':
            del_list.append(port_name)
    for port in del_list:
        region_port.remove(port)
    print(region, file = fp)
    print(region_port, file = fp)
    print("-----", file = fp)
    G.add_node(region,BID = region_root_bid,RPC = 0, Port_status = 'region')
    for node in region_port:
        G.add_node(node, BID = g.nodes[node]['switch_bid'],RPC = 0, Port_status = g.nodes[node]['Port_status'])
        G.add_edge(region,node,cost = 0)
    ##此时 region——port中只有对应的edge'端口了
    ##对于除了第一个域每一个域均需要选出一个master端口，我们应该怎么选取呢
#添加域间连线
for edge in edge_list:
    G.add_edge(edge[0],edge[1],cost = edge[2]['cost'])
print('---------开始计算域间MASTER端口-------', file = fp)
print(root_bridge.region_name, file = fp)

for node in G.nodes(data = True):
    if node[0] == root_bridge.region_name:
        continue
    print(node, file = fp)
    G.nodes[node[0]]['RPC'] = rpc(root_bridge.region_name,node[0],G)
    short_path = path(node[0],root_bridge.region_name,G)
    if node[0] in region_dict:
        master_name = short_path[1]
        region_name = short_path[0]
        g.nodes[master_name]['Port_status'] = g.nodes[master_name]['Port_status'] + ' and ' + 'master'

## 开始在域间进行选举了啊对于域间的edge进行选举DP端口 d_edge and xx


print("------------", file = fp)

for edge in G.edges(data=True):
    print(edge, file = fp)
print("------", file = fp)
for node in g.nodes(data = True):
    print(node[0], node[1]['Port_status'], file = fp)

print("------------------------------------", file = fp)


def find_switch_via_id(bid,switch_list):
    for switch in switch_list:
        if switch.bid == bid:
            return switch

for edge in edge_list:
    node1 = edge[0]
    node2 = edge[1]

    port_switch1 = find_switch_via_id(g.nodes[node1]['switch_bid'],switch_list)
    port_switch2 = find_switch_via_id(g.nodes[node2]['switch_bid'],switch_list)
    print(port_switch1.switch_name, file = fp)
    print(port_switch2.switch_name, file = fp)
    if port_switch1.region_name == root_bridge.region_name or port_switch2.region_name == root_bridge.region_name:
        #此时对应的边为主域的某一边
        if port_switch1.region_name == root_bridge.region_name:
            g.nodes[node1]['Port_status'] = g.nodes[node1]['Port_status'] + ' and ' +'DP'
        if port_switch2.region_name == root_bridge.region_name:
            g.nodes[node2]['Port_status'] = g.nodes[node2]['Port_status'] + ' and ' + 'DP'
        ##此时 master端口就是对应的根端口，我们不用从新选择了
    ##对于不是的这种情况我们的判断
    ##由于域根ID肯定不同
    else:
        if g.nodes[node1]['ERPC'] < g.nodes[node2]['ERPC']:
            g.nodes[node1]['Port_status'] = g.nodes[node1]['Port_status'] + ' and ' + 'DP'
        elif g.nodes[node1]['ERPC'] > g.nodes[node2]['ERPC']:
            g.nodes[node2]['Port_status'] = g.nodes[node2]['Port_status'] + ' and ' + 'DP'
        else:
        ##相当
            if g.nodes[node1]['Region_bridge_ID'] < g.nodes[node2]['Region_bridge_ID']:
                g.nodes[node1]['Port_status'] = g.nodes[node1]['Port_status'] + ' and ' + 'DP'
            elif g.nodes[node1]['Region_bridge_ID'] >= g.nodes[node2]['Region_bridge_ID']:
                g.nodes[node2]['Port_status'] = g.nodes[node2]['Port_status'] + ' and ' + 'DP'

    ##DP端口选择完毕

for edge in edge_list:
    node1 = edge[0]
    node2 = edge[1]
    if g.nodes[node1]['Port_status'] == 'domain_edge_port':
        g.nodes[node1]['Port_status'] = g.nodes[node1]['Port_status'] + ' and' + ' AP'
    if g.nodes[node2]['Port_status'] == 'domain_edge_port':
        g.nodes[node2]['Port_status'] = g.nodes[node2]['Port_status'] + ' and' + ' AP'


for node in g.nodes(data = True):
    print(node[0],node[1]['Port_status'], file = fp)

print('--------------完整的一棵CIST生成完毕-----------------', file = fp)
print('--------------域内的多生成树实例选取------------------', file = fp)

for node in g.nodes(data = True):
    print(node, file = fp)
#g 存储着对应的node结构
print('-------------------------------------------------', file = fp)
#每一个MSTI的实例相当于一副新的图片，因此我们可以采用新的拓扑结构


for node in g.nodes(data = True):
    print(node)

for edge in g.edges(data = True):
    print(edge)


##CIST 写入文件
print("CIST 端口角色：", file = fp2)
for node in g.nodes(data = True):
    print(node[0] + "  " + "role:" + " " + node[1]['Port_status'], file = fp2)













## 我们需要删除其中的链路 当然由于链路最优·，因此我们也可以不加删除对应的链路来进行处理

print('-----------')

## pc 与 switch 的映射
fwd_list = list() ## 存储路由表项的类
pc_list = dict() # 存储switch_name : pc_mac       —— 存储每个switch——name 对应的PC_mac地址
allPc = list() #存储所有的路由表项   存储图结构所有的PC值
mac_node_map = dict() #存储 mac ： port_ID             mac1 mac2 mac3 -------对应的PC1 PC2 PC3
mac_switch_map = dict()
for switch in switch_list:
    fwd_list.append(fwd_table(switch.switch_name)) #根据name创建对应的fwd类：对应每个switch均有一个
    str1 = str(switch.mac_list)
    list1 = str1.split(',') ## switch连接的对应PC的mac地址列表
    list1 = [str(i) for i in list1] # list1 存储对应的mac地址列表
    # mac列表相当于为 连接PC的列表
    ## 现在添加PC节点
    pc_list[switch.switch_name] = list1   #存储所有的switch_name 对应的 PC（mac地址）
    for pc in list1:
        allPc.append(pc)#名字是mac1//mac2这种的mac地址
        mac_switch_map[pc] = switch.switch_name
        mac = pc
        pc = pc[3:]
        mac_node_map[mac] = 'pc' + str(pc)
        g.add_node('pc' + str(pc), PRC = -1, Root_bridge_ID = -1, ERPC = -1, Region_bridge_ID = -1,IRPC = -1,Designated_BID = -1, Designated_PID = -1, received_PID = -1,  Port_status = 'PC', switch_bid = -1,portID = -1, Port_priority = -1, VLAN = 'none' )
        g.add_edge(switch.switch_name, 'pc' + str(pc), weight = 0, region_name = "pc_edge")
        # pc1 pc2 pc3 pc4 对应的就是 对应的PC节点 根据 mac地址 可以找到对应的节点那么

print('------已经添加了所有的节点及边---------')
print("----------增加PC节点后------------")

for edge in g.edges(data = True):
    print(edge)

for node in g.nodes(data = True):
    print(node)


## 首先计算自己的路由表项
#每个switch拥有自己的路由表项
for switch in fwd_list:
    print(switch.name + "路由表项")
    switch_name = switch.name
    ##添加自己的路由表项
    port_list = pc_list[switch_name]
    #每一步存储的都是自己的路由表项
    for pc in port_list:
        #添加自己的路由表项
        mac = pc
        node = mac_node_map[mac] # 存储mac地址对应的 PC端口的名字
        index = [mac, 0, node] ## 0 表示的是CIST
        switch.fwd_index.append(index)
        print(index)

    for pc_des in allPc:
        #需要对所有的PC均进行一遍更新
        if pc_des in port_list:
            continue
            #自己已经更新过了
        else:
            destination = mac_node_map[pc_des]   ##端口的名字
            #自己的destination 到达刚刚产生的节点的最短路径
            path1 = path(switch_name, destination,g)
            index = [pc_des, 0, path1[1]]
            switch.fwd_index.append(index)
            print(index)
            ##添加其他的所有的mac地址

print("CIST 域内的路由表项添加完毕")

##开始添加域内的路由表项



print("done")








#删除域内switch与端口互联的直线
def del_internal_edge(G,switch):
    remove_edge_list = list()
    for edge in G.edges(data = True):
        if edge[2]['cost'] ==0 and ( edge[1] == switch.switch_name or edge[2] == switch.switch_name):
            remove_edge_list.append(edge)
    G.remove_edges_from(remove_edge_list)
    return remove_edge_list
#恢复边
def recover_internal_edge(G,remove_edge_list):
    G.add_edges_from(remove_edge_list)

#删除VLAN不能传播的链路
def remove_VLAN_edge(G, edge, vlan_range):
    vlan_range = vlan_range.split('-')
    #存储对应的上限和下限
    vlan_range = list(map(int, vlan_range))
    port1 = edge[0]
    port2 = edge[1]
    # vlan1 2 为edge 端口两端对应的vlan通过情况
    vlan1 = G.nodes[port1]['VLAN']
    vlan2 = G.nodes[port2]['VLAN']
    if vlan1 == 'none' or vlan2 == 'none' :
        return 'true'
    vlan1 = vlan1.split('-')
    vlan2 = vlan2.split('-')
    vlan1 = list(map(int, vlan1))
    vlan2 = list(map(int, vlan2))
    #vlan 为edge所能通过的vlan
    #取可以通过的子集
    vlan = list()
    vlan.append(max(vlan1[0], vlan2[0]))
    vlan.append(min(vlan1[1], vlan2[1]))
    if vlan[0]<= vlan_range[0] and vlan[1] >= vlan_range[1]:
        return 'true'
    else:
        return 'false'
    #存储可以通过的vlan

    #如果可以通过则返回对应的vlan，否则返回不能通过的vlan格式









print(region_dict, file = fp)
print('----------------', file = fp)
raw_data = pd.read_excel(file_path, header=0, sheet_name='VLAN')
data = raw_data.values
for i in range(data.shape[0]):
    port_data = data[i]
    print(port_data, file = fp)
    region_name = port_data[0]
    MSTI_name = port_data[1]
    vlan_range = port_data[2]
    MSTI_bridge = port_data[3]
    root_bridge = find_switch(MSTI_bridge)
    target_switch = root_bridge
    # 优先级置为0
    MSTI_BID = root_bridge.mac

    switch_name_list = region_dict[region_name]
    print(switch_name_list, file = fp)
    switch_list1 = list()
    switch_portlist = list()
    for switch_name in switch_name_list:
        switch_list1.append(find_switch(switch_name))
    for switch in switch_list1:
        for port in switch.port:
            port_name = switch.switch_name + '-' + str(port)
            switch_portlist.append(port_name)
    #在新的图形中添加消息 每次会重新添加一次
    region_g = nx.Graph()
    root_switch_bid = 0
    list_node = list()
    for node in g.nodes(data = True):
        if node[0] in switch_name_list:
            list_node.append(node)
        if node[0] in switch_portlist:
            list_node.append(node)
    region_g.add_nodes_from(list_node)
    backup_node = list()
    for node in region_g.nodes(data = True):
        ##修改端口角色的状态：
        region_g.nodes[node[0]]['Root_bridge_ID'] = MSTI_BID
        region_g.nodes[node[0]]['Region_bridge_ID'] = MSTI_BID
        region_g.nodes[node[0]]['IRPC'] = 0
        region_g.nodes[node[0]]['ERPC'] = 0
        region_g.nodes[node[0]]['Designated_BID'] = node[1]['switch_bid']
        region_g.nodes[node[0]]['Designated_PID'] = node[1]['PID']
        region_g.nodes[node[0]]['received_PID'] = 0
        if region_g.nodes[node[0]]['Port_status'] == 'backup':
            backup_node.append(node[0])
            continue
        else:
            if region_g.nodes[node[0]]['Port_status'][0:6] == 'domain':
                region_g.nodes[node[0]]['Port_status'] = 'domain_edge_port'
            elif region_g.nodes[node[0]]['Port_status'] == 'switch':
                continue
            else :
                region_g.nodes[node[0]]['Port_status'] = 'none'
    ## 添加边
    ###这里删除不能转播此VLAN的边

    edge_list = list()
    for edge in g.edges(data=True):
        if edge[2]['region_name'] == region_name and edge[0] not in backup_name and edge[1] not in backup_name and edge[2]['region_name'] != 'pc_edge':
            edge_list.append(edge)
    region_g.add_edges_from(edge_list)

    for edge in region_g.edges(data = True):
        res = remove_VLAN_edge(region_g, edge, vlan_range)
        if res == 'false':
            region_g.remove_edge(edge[0],edge[1])
        else:
            continue
    #开始选拔端口
    ##阻塞备份端口的节点
    print('{}域 MSTI{} 根桥为 {}'.format( region_name ,MSTI_name, MSTI_bridge), file = fp)
    ##根桥的所有非域间端口变成 DP
    for node in region_g.nodes(data = True):
        if root_bridge.bid == node[1]['switch_bid'] and node[1]['Port_status'] != 'domain_edge_port' and node[1]['Port_status'] != 'backup' and node[1]['Port_status'] != 'switch':
            region_g.nodes[node[0]]['Port_status'] = 'DP'
    ##计算根端口
    for switch in switch_list1:
        if switch == root_bridge:
            continue
        else:
            #断开端口间的连线
            remove_edge_list = del_internal_edge(region_g, switch)
            port_list = switch.port
            for port in port_list:
                port_name = switch.switch_name + '-' + str(port)
                if switch.switch_name + '-' + str(port) in backup_name:
                    continue
                if port_name in domain_edge_list:
                    continue
                ##此时不为边缘端口且不为备份端口需要进行计算
                min_num = 9999999
                Designated_port_name = str()
                for j in target_switch.port:
                    port_name2 = target_switch.switch_name + '-' + str(j)
                    if port_name2 in backup_name :
                        continue
                    if port_name2 in domain_edge_list:
                        continue
                    p1 = rpc(port_name, port_name2, region_g)
                    if min_num > p1:
                        min_num = p1
                        print('{}{}为{}'.format(port_name, port_name2, min_num), file = fp)
                        # 更优秀
                        short_path = path(port_name, port_name2, region_g)
                        print(short_path, file = fp)
                        Designated_port_name = short_path[1]

                ##此时我们需要进行更新BPDU
                region_g.nodes[port_name]['IRPC'] = min_num
                region_g.nodes[port_name]['Designated_BID'] = find_designated_bridge(Designated_port_name)
                region_g.nodes[port_name]['Designated_PID'] = find_designated_pid(Designated_port_name)
                region_g.nodes[port_name]['received_PID'] = find_self_pid(port_name)
            recover_internal_edge(region_g,remove_edge_list)
        ##此时内部的IRPC更新完毕，为非根桥依次选取根端口：
    print('--------------------域内MSTI BPDU更新完毕开始选取根端口-----------------', file = fp)
    for switch in switch_list1:
        # 对于域内根桥已经选取结束
        if switch == root_bridge:
            continue
        ##开始选举
        rootport = ''
        #找到第一个优先级最高的节点
        for i in switch.port:
            port_name = switch.switch_name + '-' + str(i)
            if port_name in backup_name:
                continue
            if port_name in domain_edge_list:
                continue
            rootport = port_name
            break

        for i in switch.port:
            port_name = switch.switch_name + '-' + str(i)
            if port_name in backup_name:
                continue
            if port_name in domain_edge_list:
                continue
            if region_g.nodes[port_name]['IRPC'] < region_g.nodes[rootport]['IRPC']:
                rootport = port_name
            elif region_g.nodes[port_name]['IRPC'] > region_g.nodes[rootport]['IRPC']:
                pass
            elif region_g.nodes[port_name]['IRPC'] == region_g.nodes[rootport]['IRPC']:
                if region_g.nodes[port_name]['Designated_BID'] < region_g.nodes[rootport]['Designated_BID']:
                    rootport = port_name
                elif region_g.nodes[port_name]['Designated_BID'] == region_g.nodes[rootport]['Designated_BID']:
                    if region_g.nodes[port_name]['Designated_PID'] < region_g.nodes[rootport]['Designated_PID']:
                        rootport = port_name
                    elif region_g.nodes[port_name]['Designated_PID'] == region_g.nodes[rootport]['Designated_PID']:
                        if region_g.nodes[port_name]['received_PID'] < region_g.nodes[rootport]['received_PID']:
                            rootport = port_name

        region_g.nodes[rootport]['Port_status'] = 'Root Port'
    print("--------域内ROOT PORT选拔完毕---------", file = fp)
    print('--------开始选取DP端口----------------', file = fp)
    print("-------根据选拔跟端口信息进行更新配置BPDU信息选拔DP-------", file = fp)
    for switch in switch_list1:
        if switch == root_bridge:
            continue
        ##开始选举DP端口
        ##switch 不是域根
        port_list = switch.port
        min_cost = 999999
        #更新switch到域根最小的IRPC
        for port in port_list:
            port_name = switch.switch_name + '-' + str(port)
            if switch.switch_name + '-' + str(port) in backup_name:
                continue
            if region_g.nodes[port_name]['Port_status'] == 'domain_edge_port':
                # 域间的不进行更新
                continue
            if min_cost > region_g.nodes[port_name]['IRPC']:
                min_cost = region_g.nodes[port_name]['IRPC']
        # 更新出switch中最小的
        for port in port_list:
            if switch.switch_name + '-' + str(port) in backup_name:
                continue
            port_name = switch.switch_name + '-' + str(port)
            if region_g.nodes[port_name]['Port_status'] == 'domain_edge_port':
                # 域间的不进行更新
                continue
            region_g.nodes[port_name]['IRPC'] = min_cost
            region_g.nodes[port_name]['Designated_BID'] = switch.bid
            region_g.nodes[port_name]['Designated_PID'] = region_g.nodes[port_name]['PID']
    print('------------域内BPDU更新完毕，开始选举DP端口------------', file = fp)
    DP_list = list()
    for port in root_bridge.port:
        portName = root_bridge.switch_name + '-' + str(port)
        if region_g.nodes[portName]['Port_status'] == 'domain_edge_port':
            # 不更新
            continue
        if region_g.nodes[portName]['Port_status'] == 'backup':
            continue
        DP_list.append(portName)
    # DP_list存储着域内为DP的端口
    for edge in region_g.edges(data=True):
        if edge[0] in DP_list or edge[1] in DP_list or edge[2]['cost'] == 0:
            # 指定端口已经选举
            continue
        if region_g.nodes[edge[0]]['IRPC'] < region_g.nodes[edge[1]]['IRPC']:
            region_g.nodes[edge[0]]['Port_status'] = 'DP'
        elif region_g.nodes[edge[0]]['IRPC'] > region_g.nodes[edge[1]]['IRPC']:
            region_g.nodes[edge[1]]['Port_status'] = 'DP'
        elif region_g.nodes[edge[0]]['IRPC'] == region_g.nodes[edge[1]]['IRPC']:
            if region_g.nodes[edge[0]]['Designated_BID'] < region_g.nodes[edge[1]]['Designated_BID']:
                region_g.nodes[edge[0]]['Port_status'] = 'DP'
            elif region_g.nodes[edge[0]]['Designated_BID'] > region_g.nodes[edge[1]]['Designated_BID']:
                region_g.nodes[edge[1]]['Port_status'] = 'DP'
            else:
                if region_g.nodes[edge[0]]['Designated_PID'] < region_g.nodes[edge[1]]['Designated_PID']:
                    region_g.nodes[edge[0]]['Port_status'] = 'DP'
                elif region_g.nodes[edge[0]]['Designated_PID'] > region_g.nodes[edge[1]]['Designated_PID']:
                    region_g.nodes[edge[1]]['Port_status'] = 'DP'

    for node in region_g.nodes(data = True):
        if node[1]['Port_status'] == 'none':
            region_g.nodes[node[0]]['Port_status'] = 'AP'
    print('------AP端口选择完毕----------', file = fp)

    print('-------下方为所有node对应的状态---------', file = fp)
    print(' ',file = fp2)
    print('{}域 MSTI{} VLAN端口角色划分如下'.format(region_name, MSTI_name, MSTI_bridge), file = fp)
    print('---------------------------------------------------------', file = fp2)
    print('{}域 MSTI{} VLAN端口角色划分如下'.format(region_name, MSTI_name, MSTI_bridge), file=fp2)
    for edge in region_g.edges(data=True):
        print(edge, file = fp)

    print('-----------------------------', file = fp)

    for node in region_g.nodes(data = True):
        print(node, file = fp)
        print(node[0] + "  " + "role:" + " " + node[1]['Port_status'], file=fp2)
    print('-----------------------------', file = fp)
    #仅仅包含其bid
    print('------', file = fp)

    for edge in region_g.edges(data=True):
        print(edge)
    print('-----------------------------')
    for node in region_g.nodes(data = True):
        print(node)
    print('-----------------------------')
    #vlan_range 表示对应的vlan号为多少
    #现在需要给每一个switch添加MSTI的域内表项

    #需要找到域内的PC mac地址
    region_mac = list()

    ## 删除对应的线路：
    del_edge = list()
    for edge in region_g.edges(data = True):
        if region_g.nodes[edge[0]]['Port_status'] == 'AP' or region_g.nodes[edge[1]]['Port_status'] == 'AP' :
            del_edge.append(edge)
    for edge in del_edge:
        region_g.remove_edge(edge[0], edge[1])

    #记录域内所有的mac地址
    all_mac = list()
    for switch in switch_list1:
        str1 = str(switch.mac_list)
        list1 = str1.split(',')  ## switch连接的对应PC的mac地址列表
        list1 = [str(i) for i in list1]  # list1 存储对应的mac地址列表
        for mac in list1:
            all_mac.append(mac)
    port_list = list()
    for switch in fwd_list:
        # 只添加自己域内的 index
        if switch.name not in switch_name_list:
            continue
        print(switch.name + "路由表项" + "更新 :")
        switch_name = switch.name
        ##添加自己的路由表项
        port_list = pc_list[switch_name]
        ## index = [mac, VLAN_ID, port_ex]
        # 每一步存储的都是自己的路由表项
        # 只用更新域内的MSTI

        # 首先添加自己的路由表项
        for pc in port_list:
            mac = pc
            node = mac_node_map[mac]  # 存储mac地址对应的 PC端口的名字
            index = [mac, vlan_range, node]  ## 0 表示的是CIST
            switch.fwd_index.append(index)
            print(index)
            # 自己的路由项添加完毕

        for pc_des in all_mac:
            # 需要对所有的PC均进行一遍更新
            if pc_des in port_list:
                continue
                # 自己已经更新过了
            else:
                destination = mac_switch_map[pc_des]  ##端口的名字
                # 自己的destination 到达刚刚产生的节点的最短路径
                path1 = path(switch_name, destination, region_g)
                index = [pc_des, vlan_range, path1[1]]
                switch.fwd_index.append(index)
                print(index)
                ##添加其他的所有的mac地址



        ##region_g 中的线路

    ## 恢复对应的edge
    region_g.add_edges_from(del_edge)



    print("CIST 域内的路由表项添加完毕")
fp1 = open('/Users/yewen/Desktop/2023毕业设计/code/STP/data_test/mac_table.txt', "w")
for switch in fwd_list:
    list_fwd = switch.fwd_index
    n = len(list_fwd)
    print(switch.name + " MAC表如下：", file = fp1)
    for i in range(n):
        print(list_fwd[i], file = fp1)
    print("   ", file = fp1)
fp1.close()



fp.close()
fp2.close()


end = time.time()

print("时间：", end- start)
'''
print('-------------------')
for edge in g.edges(data = True):
    print(edge)

print('------------------')

for node in g.nodes(data = True):
    print(node)




        #目前G的图片全部完成，我们需要绘制对应的


'''




    ##开始选拔域
    # 间DP端口，针对的是每个线路
    # 需要重新计算RPC
    ## 根据跟端口的信息来进行替换为自己的ID

    # for node in g.nodes(data=True):
    #   print(node)

    ####### code section


"""
##添加edge
for edge in edge_list:
    g.add_edges_from([ (edge[0],edge[1],edge[2]) ])

for edge in g.edges(data=True):
     print(edge)
"""

##添加域间路由
