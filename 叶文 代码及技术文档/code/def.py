

# -*- coding: utf-8 -*-
# #define for picture

'''
根端口的选举规则是：依次比较各端口的RPC、发送者BID、发送端口PID和接收端口PID，较小者对应的端口成为根端口；
指定端口的选举规则是：依次比较所在交换机的RPC、所在交换机的BID和本端口的PID，较小者对应的端口成为指定端口。
'''
import pandas as pd
import time
import networkx as nx
import matplotlib.pyplot as plt
import PIL

import matplotlib
g = nx.Graph() # 创建拓扑图
G = nx.Graph()
#增加节点 节点是端口
#NO 增加

##建立交换机类
print("-------添加节点中--------")
class Switch:
    def __init__(self, port_list, number, switch_name):
        self.port = []
        self.switch_name = switch_name
        for i in port_list:
            self.port.append(i)
        self.number = number ## switch bid
file_path = '/Users/yewen/Desktop/2023毕业设计/code/switch1.xlsx'
raw_data = pd.read_excel(file_path, header=0, sheet_name='switch')
data = raw_data.values
switch_list = list()
## 读取execl switch信息
for i in range(data.shape[0]) :
    switch_data = data[i]
    str1 = str(switch_data[0])
    list1 = str1.split(',')
    list1 = [int(i) for i in list1]
    print(list1)
    switch_list.append(Switch(list1, switch_data[1], switch_data[2]))



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
    g.add_node(port_data[0],RPC = port_data[1],SBID = port_data[2], BID = port_data[3], SPID = port_data[0],Port_status = port_data[5])
##数据维修
for switch in switch_list:
    port_list = switch.port
    for port in port_list:
        g.nodes[port]['SBID'] = switch.number
        g.nodes[port]['BID'] = switch.number
    g.add_node(switch.switch_name,RPC = -1, SBID = -1, BID = switch.number, SPID = -1, Port_status = 'Switch')


for node in g.nodes(data = True):
    print(node)
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
     print(edge)
##############

print('----节点添加完成')
#选举根桥
# 选择 rootNode 找到对应的 root 可能对应多个端口
print('----选举根桥-----')
time.sleep(0.5)
rootNode = 9999 #max
for node in g.nodes(data = True):
    if rootNode > node[1]['BID'] :
        rootNode = node[1]['BID']
print("THE rootNode  BID is {}".format(rootNode))


##此时直接根据这个来选择BID



#更新配置的BPDU
print("------更新配置的BPDU------")
time.sleep(0.5)
#更改BPDU的 BID status
for node in g.nodes(data = True):
    if node[1]['BID'] == rootNode and node[1]['Port_status'] != 'Switch':
        g.nodes[node[0]]['Port_status'] = "Designated"
    node[1]['BID'] = rootNode
    print(node)
else:
    print("the alter BID action is over")






print("---------寻找root Port------计算RPC-----")
time.sleep(0.5)
#寻找root Port 计算RPC
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
#rootNode 为BID
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
    print(edge)
print("##########")



## 已经算出了所有port 对应的rpc 接下来我们需要判断 RP
print('-------更新结果如下---------')
for node in g.nodes(data = True):
    print(node)
#########################此时节点的BPDU更新完毕
## judge for RP 每个跟端口有且只有唯一一个
print('------选举RootPort-----')
time.sleep(0.5)

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
    print(node)

## 此时已经交换完成了 我们可以用来选举DP 指定端口的选举

## DP 的选择是根据 路由器之间 为一个网段，每个网段选举出一个指定端口 比较SBID SPID 来进行决定
## 先比较 RPC
print('-----重新计算RPC------')
time.sleep(0.2)
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







print('-----选举指定端口DP------')
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
    print(node)
## 端口更新成功
print("端口状态更新成功")
print("-------选举堵塞AP端口------")
time.sleep(0.5)
for node in g.nodes.data():
    if node[1]['Port_status'] == 'None' :
        ##此时为AP
        node[1]['Port_status'] = 'AP'
print('-------打印最终结果-------')
for node in g.nodes(data = True):
    print(node)
print("##3种端口状态及根桥更新完毕##")

##开始画图：

print('-----拓扑图更新-----')
icons = {
"switch": '/Users/yewen/Desktop/2023毕业设计/code/switch_node.png'
}
# Load images
images = {k: PIL.Image.open(fname) for k, fname in icons.items()}


port_ap = list()
for switch in switch_list:
    port_list = switch.port
    G.add_node(switch.switch_name, BID=switch.number, Port_status='Switch', image=images['switch'])
    for port in port_list:
        if g.nodes[port]['Port_status'] =='AP':
            G.add_node(switch.switch_name, BID=switch.number, Port_status='Switch_AP', image=images['switch'])
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
print("########")
edge_list_red = list()
edge_list_blue = list()
## blue 为存储AP的端口
for edge in G.edges(data = True):
    if edge[2]['AP'] == 'false' :
        edge_list_red.append((edge[0],edge[1]))
    if edge[2]['AP'] == 'true' :
        edge_list_blue.append((edge[0], edge[1]))
    print(edge)



print("-------节点分类-----")


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



plt.title("title")
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


plt.show()

