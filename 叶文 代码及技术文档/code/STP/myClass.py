

#switch 类，用于网路拓扑图中对于switch的创建，包含了swith port列表，switch_name,switch BID
class Switch:
    def __init__(self, port_list, number, switch_name):
        self.port = []
        self.switch_name = switch_name
        for i in port_list:
            self.port.append(i)
        self.number = number ## switch bid

## read_file 类：用于读取创建的execl文件，生成网络拓扑图
class read_file:
    def __int__(self, file_path):
        self.file_path = file_path