
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : ${DATE} ${TIME}

import pandas as pd
import time
import networkx as nx
import matplotlib.pyplot as plt
import PIL
start = time.time()
fp = open('/Users/yewen/Desktop/2023毕业设计/code/STP/data_test/print.txt',"w")
import matplotlib
g = nx.Graph() # 创建拓扑图
G = nx.Graph()
#增加节点 节点是端口
# 增加

##建立交换机类
print("-------添加节点中--------", file = fp)
class Switch:
    def __init__(self, port_list, number, switch_name, pc_mac = 0):
        self.port = []
        self.switch_name = switch_name
        for i in port_list:
            self.port.append(i)
        self.number = number ## switch bid
        self.pc_mac = pc_mac

class fwd_table:
    def __init__(self, switch_name):
        self.name = switch_name
        self.fwd_index = list()

file_path = '/Users/yewen/Desktop/2023毕业设计/code/STP/data_test/stp.xls'
raw_data = pd.read_excel(file_path, header=0, sheet_name='switch')
data = raw_data.values
switch_list = list()
## 读取execl switch信息
for i in range(data.shape[0]) :
    switch_data = data[i]
    str1 = str(switch_data[0])
    list1 = str1.split(',')
    list1 = [int(i) for i in list1]
    print(list1, file = fp)
    switch_list.append(Switch(list1, switch_data[1], switch_data[2],switch_data[3]))



'''
##输入节点 之后进行修改
list_Node = input()
g.add_nodes_from(list_Node)
'''
# 对于4节点的拓扑图 8 个节点 初始化BPDU 端口初始化
raw_data = pd.read_excel(file_path, header=0, sheet_name='port')
data = raw_data.values
for i in range(data.shape[0]) :
    port_data = data[i]
    g.add_node(port_data[0],RPC = 0,SBID = 0, BID = 0, SPID = port_data[1],Port_status = 'None')
##数据维修
for switch in switch_list:
    port_list = switch.port
    for port in port_list:
        g.nodes[port]['SBID'] = switch.number
        g.nodes[port]['BID'] = switch.number
    g.add_node(switch.switch_name,RPC = -1, SBID = -1, BID = switch.number, SPID = -1, Port_status = 'Switch')


for node in g.nodes(data = True):
    print(node, file = fp)
#初始化边
for switch in switch_list :
    #根据路由器来添加节点
    port_list = switch.port
    switchname = switch.switch_name
    for port in port_list :
        g.add_weighted_edges_from([(port,switchname,0)])

##############

raw_data = pd.read_excel(file_path, header=0, sheet_name='edge')
data = raw_data.values

for i in range(data.shape[0]) :
    list1 = list(data[i])
    g.add_weighted_edges_from([(list1[0],list1[1],list1[2])])
for edge in g.edges(data = True):
    if edge[2]['weight'] != 0:
     print(edge, file = fp)
##############

print('----节点添加完成', file = fp)
#选举根桥
# 选择根节点找到对应的根可能对应多个端口
print('----选举根桥-----', file = fp)

rootNode = 9999 #max
for node in g.nodes(data = True):
    if rootNode > node[1]['BID'] :
        rootNode = node[1]['BID']
print("THE rootNode  BID is {}".format(rootNode), file = fp)


##此时直接根据这个来选择BID



#更新配置的BPDU
print("------更新配置的BPDU------", file = fp)

#更改BPDU状态
for node in g.nodes(data = True):
    if node[1]['BID'] == rootNode and node[1]['Port_status'] != 'Switch':
        g.nodes[node[0]]['Port_status'] = "Designated"
    node[1]['BID'] = rootNode
    print(node, file = fp)
else:
    print("the alter BID action is over", file = fp)






print("---------寻找root Port------计算RPC-----", file = fp)

#寻找根端口计算RPC
#内置算法
def rpc(node1, node2):
    #断开对应的端口计算
    p = nx.shortest_path_length(g,source = node1, target = node2, weight = 'weight' )
    return p

def path(node1,node2):
    p = nx.shortest_path(g, source = node1, target = node2, weight = 'weight')
    return p

def find_bid(port1): #参数为端口
    for switch in switch_list:
        if port1 in switch.port:
            return switch.number

#更新rpc 与配置 BPDU
#根节点为BID
target_switch = Switch([],-1,'-1')
for switch in switch_list:
    #找到对应的switch
    if switch.number == rootNode:
        target_switch = switch
        break


for switch in switch_list: #更改 定义端口数量
    if switch == target_switch:
        continue;
    #交换机 存储着BID 对应端口的PID 我们需要对每个端口计算到BP的距离
    port_list = switch.port
    switchname = switch.switch_name
    #去掉端口的边
    for i in port_list:
        if g.has_edge(i,switchname):
            g.remove_edge(i,switchname)

    #更新完成计算rpc
    #对port_list 计算
    for i in port_list:
        min = 999999
        for j in target_switch.port:
                p1 = rpc(i,j)
                if min > p1:
                    min = p1
                    #更优秀
                    short_path = path(i,j)
                    sbid = find_bid(short_path[1])

        #计算出来后需要修改
        g.nodes[i]['RPC'] = min
        g.nodes[i]['SPID'] = short_path[1]
        g.nodes[i]['SBID'] = sbid
    #恢复线路
    for i in port_list:
        if not g.has_edge(i,switchname) :
                     g.add_weighted_edges_from([(i,switchname,0)])

for edge in g.edges(data=True):
    print(edge, file = fp)
print("##########", file = fp)



## 已经算出了所有port 对应的rpc 接下来我们需要判断 RP
print('-------更新结果如下---------', file = fp)
for node in g.nodes(data = True):
    print(node, file = fp)
#########################此时节点的BPDU更新完毕
## r RP 每个跟端口有且只有唯一一个
print('------选举RootPort-----', file = fp)


for swith in switch_list:
    if swith == target_switch:
        continue
    ##开始选举
    rootport = swith.port[0] ## 指明第一个端口
    for i in swith.port:
        if g.nodes[i]['RPC'] < g.nodes[rootport]['RPC']:
            rootport = i
        elif g.nodes[i]['RPC'] == g.nodes[rootport]['RPC'] :
            if g.nodes[i]['SBID'] < g.nodes[rootport]['SBID']:
                rootport = i
    g.nodes[rootport]['Port_status'] = 'Root Port'

for node in g.nodes(data = True):
    print(node, file = fp)

## 此时已经交换完成了 我们可以用来选举DP 指定端口的选举

## DP 的选择是根据 路由器之间 为一个网段，每个网段选举出一个指定端口 比较SBID SPID 来进行决定
## 先比较 RPC
print('-----重新计算RPC------', file = fp)

#######################################DP


### 此时不进行切边，我们需要对链路的RPC重新计算
for switch in switch_list:
    port_list = switch.port
    min = 99999
    for port in port_list:
        if g.nodes[port]['RPC'] < min:
            min = g.nodes[port]['RPC']
    for port in port_list:
        g.nodes[port]['RPC'] = min
target_port = target_switch.port
for switch in switch_list:
    if switch == target_switch:
        continue
    else:
        port_list  =switch.port
        for port in port_list:
            g.nodes[port]['SPID'] = port
            g.nodes[port]['SBID'] = switch.number


print('-----选举指定端口DP------', file = fp)
#对边进行判断
port_list = target_switch.port #这些端口已经为DP
for edge in g.edges.data():
    if edge[0] in port_list or edge[1] in port_list :
        # 指定端口已经选举
        continue
    if(edge[2]['weight'] == 0):
        continue
    #此时未选举
    if g.nodes[edge[0]]['RPC'] < g.nodes[edge[1]]['RPC']:
        g.nodes[edge[0]]['Port_status'] = 'Designated'
    elif g.nodes[edge[0]]['RPC'] > g.nodes[edge[1]]['RPC']:
        g.nodes[edge[1]]['Port_status'] = 'Designated'
    else:
        #对比SBID
        if g.nodes[edge[0]]['SBID'] < g.nodes[edge[1]]['SBID']:
            g.nodes[edge[0]]['Port_status'] = 'Designated'
        elif g.nodes[edge[0]]['SBID'] > g.nodes[edge[1]]['SBID']:
            g.nodes[edge[1]]['Port_status'] = 'Designated'
        else:
            if g.nodes[edge[0]]['SPID'] < g.nodes[edge[1]]['SPID']:
                g.nodes[edge[0]]['Port_status'] = 'Designated'
            elif g.nodes[edge[0]]['SPID'] > g.nodes[edge[1]]['SPID']:
                g.nodes[edge[1]]['Port_status'] = 'Designated'

for node in g.nodes(data = True):
    print(node, file = fp)
## 端口更新成功
print("端口状态更新成功", file = fp)
print("-------选举堵塞AP端口------", file = fp)

apPort_list = list()
for node in g.nodes.data():
    if node[1]['Port_status'] == 'None' :
        ##此时为AP
        node[1]['Port_status'] = 'AP'
        apPort_list.append(node[0])
print('-------打印最终结果-------', file = fp)
for node in g.nodes(data = True):
    print(node, file = fp)
print("##3种端口状态及根桥更新完毕##", file = fp)


for node in g.nodes(data = True):
    print(node)
fp2 = open('/Users/yewen/Desktop/2023毕业设计/code/STP/data_test/role.txt', "w")
for node in g.nodes(data = True):
    print(str(node[0])+ " " + "role: " + node[1]['Port_status'], file = fp2)
fp2.close()

for edge in g.edges(data = True):
    print(edge)

edge_remove = list()
for edge in g.edges(data = True):
    port1 = edge[0]
    port2 = edge[1]
    if edge[2]['weight'] == 0:
        continue
    else:
        if port1 in apPort_list or port2 in apPort_list:
            edge_remove.append(edge)

for edge in edge_remove:
    g.remove_edge(edge[0], edge[1])

print('开始计算MAC转发表')

fwdTable_list = list()
pc_list = dict()
allPc = list()
mac_node_map = dict()
for switch in switch_list:
    fwdTable_list.append(fwd_table(switch.switch_name))
    str1 = str(switch.pc_mac)
    list1 = str1.split(',')
    list1 = [str(i) for i in list1]
    ## 现在添加PC节点
    pc_list[switch.switch_name] = list1
    for pc in list1:
        allPc.append(pc)
        mac = pc
        pc = pc[3:]
        mac_node_map[mac] = 'pc' + str(pc)
        g.add_node('pc' + str(pc), PRC = -1, SBID = -1, SPID = -1, Port_status = 'PC' )
        g.add_edge(switch.switch_name, 'pc' + str(pc), weight = 0)

print("----------增加PC节点后------------")

for edge in g.edges(data = True):
    print(edge)

for node in g.nodes(data = True):
    print(node)

#index MAC-地址——————————————VLANID----------PORT

for switch in fwdTable_list:
    print(switch.name + "路由表项")
    switch_name = switch.name
    ##添加自己的路由表项
    port_list = pc_list[switch_name]
    for pc in port_list:
        #添加自己的路由表项
        mac = pc
        node = mac_node_map[mac]
        index = [mac, 0, node]
        switch.fwd_index.append(index)
        print(index)

    for pc_des in allPc:
        if pc_des in port_list:
            continue
        else:
            destination = mac_node_map[pc_des]
            path1 = path(switch_name, destination)
            index = [pc_des, 0, path1[1]]
            switch.fwd_index.append(index)
            print(index)










for edge in edge_remove:
    g.add_edge(edge[0], edge[1], weight = edge[2]['weight'])

print('---------MAC转发表添加完毕-------------')




##开始画图：

print('-----拓扑图更新-----', file = fp)
icons = {
"switch": '/Users/yewen/Desktop/2023毕业设计/code/switch_node.png'
}
# Load images
images = {k: PIL.Image.open(fname) for k, fname in icons.items()}


port_ap = list()
macALL = list()
for switch in switch_list:
    port_list = switch.port
    str1 = str(switch.pc_mac)
    list1 = str1.split(',')
    list1 = [str(i) for i in list1]
    for i in list1:
        macALL.append(i)
    G.add_node(switch.switch_name, BID=switch.number, Port_status='Switch', image=images['switch'], fwd_mac = list1, fwding = list())
    for port in port_list:
        if g.nodes[port]['Port_status'] =='AP':
            G.add_node(switch.switch_name, BID=switch.number, Port_status='Switch_AP', image=images['switch'], fwd_mac= list1, fwding = list())
            port_ap.append(port)



for edge in g.edges(data = True):
    if edge[2]['weight'] == 0 :
        continue
    weight = edge[2]['weight']
    flag = 0
    if g.nodes[edge[0]]['Port_status'] == 'AP' or g.nodes[edge[1]]['Port_status'] == 'AP':
        flag = 1
    pair = list()
    pair_name = list()
    pair.append(edge[0])
    pair.append(edge[1])
    ##寻找


    for port in pair:
        for switch in switch_list:
            if port in switch.port:
                pair_name.append(switch.switch_name)
    ##找到了
    G.add_edge(pair_name[0], pair_name[1], weight = weight, AP = 'false', color = 'blue')
    if flag == 1:
        G[pair_name[0]][pair_name[1]]['AP'] = 'true'


for node in G.nodes(data = True):
    print(node)
for edge in G.edges(data = True):
    print(edge)
##开始学习MAC表


## 未每个switch分配mac学习表

print("########", file = fp)
edge_list_red = list()
edge_list_blue = list()
## blue 为存储AP的端口
for edge in G.edges(data = True):
    if edge[2]['AP'] == 'false' :
        edge_list_red.append((edge[0],edge[1]))
    if edge[2]['AP'] == 'true' :
        edge_list_blue.append((edge[0], edge[1]))
    print(edge, file = fp)

## G 中存储着对应的switch节点
## switch_list 存储对应接口的具体消息


print("-------节点分类-----")


fp1 = open('/Users/yewen/Desktop/2023毕业设计/code/STP/data_test/mac_table.txt', "w")
for switch in fwdTable_list:
    list_fwd = switch.fwd_index
    n = len(list_fwd)
    print(switch.name + " MAC表如下：", file = fp1)
    for i in range(n):
        print(list_fwd[i], file = fp1)
    print("   ", file = fp1)
fp1.close()







end = time.time()
print("总的时间为：", end - start)

'''
###开始画图

pos = nx.spring_layout(G, seed=1734289230)
fig, ax = plt.subplots()



##对线进行处理
nx.draw_networkx_edges(
    G,
    pos=pos,
    edgelist = edge_list_red,
    ax=ax,
    arrows=True,
    arrowstyle="-",
    min_source_margin=15,
    min_target_margin=15,
    edge_color="tab:red",

)
nx.draw_networkx_edges(
    G,
    pos=pos,
    edgelist = edge_list_blue,
    ax=ax,
    arrows=True,
    arrowstyle="]-[",
    min_source_margin=15,
    min_target_margin=15,
    edge_color="tab:blue",
)

#设置字体为楷体



plt.title("STP result")
tr_figure = ax.transData.transform
tr_axes = fig.transFigure.inverted().transform
icon_size = (ax.get_xlim()[1] - ax.get_xlim()[0]) * 0.025
icon_center = icon_size / 2.0
for n in G.nodes:
    xf, yf = tr_figure(pos[n])
    xa, ya = tr_axes((xf, yf))
    # get overlapped axes and plot icon
    a = plt.axes([xa - icon_center, ya - icon_center, icon_size, icon_size])
    a.imshow(G.nodes[n]["image"],)
    a.axis("off")
    plt.title(n)
fp.close()
plt.savefig('/Users/yewen/Desktop/2023毕业设计/code/STP/data_test/stp.png')
plt.show()

'''
###开始画图
