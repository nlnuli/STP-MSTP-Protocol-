#定义switch,包含了对应的端口列表，name，mac，priority，region——name

class Switch:
    #port端口，name，mac，priority，bid
    def __init__(self, port_list, mac, switch_name, priority,region_name):
        self.port = []
        self.switch_name = switch_name
        for i in port_list:
            self.port.append(i)
        self.mac = mac ## switch bid
        self.priority = priority
        self.bid = int(str(self.priority) + str(self.mac)) #bid 代表优先级
        self.region_name = region_name


## read_file 类：用于读取创建的execl文件，生成网络拓扑图
class read_file:
    def __int__(self, file_path):
        self.file_path = file_path

