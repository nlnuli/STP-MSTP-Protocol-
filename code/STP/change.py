# 在代码中添加如下语句 —— 设置字体为：SimHei（黑体）



import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline
from matplotlib.font_manager import FontProperties
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']



# plot double lines
def plot_double_lines(n, x, y1, pic_name):
    # initialize plot parameters
    plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']

    print('picture name: %s, len of data: %d' % (pic_name, n))
    plt.rcParams['figure.figsize'] = (10 * 16 / 9, 10)
    plt.subplots_adjust(left=0.06, right=0.94, top=0.92, bottom=0.08)

    # 对x和y1进行插值
    x_smooth = np.linspace(x.min(), x.max(), 50)
    y1_smooth = make_interp_spline(x, y1)(x_smooth)
    # plot curve 1
    plt.plot(x, y1,marker="d",label="MSTP算法效率", color='b', linewidth=4,markersize=10, alpha=0.5)

    # show the legend
    plt.tick_params(labelsize=23)
    plt.rcParams.update({'font.size': 18})
    plt.legend(loc = 'lower right')

    font2 = {'family': 'Arial Unicode MS',
             'weight': 'normal',
             'size': 20,
             }
    plt.xlabel('节点数量/个', font2)
    plt.ylabel('执行时间/S', font2)
    xx = [4, 10 , 16, 25, 37, 46, 60 ]
    yy = [0.065, 0.082, 0.10, 0.12, 0.16, 0.21, 0.3]
    # show the picture
    plt.savefig("test1.svg", dpi=600, format="svg")
    plt.show()



if __name__ == '__main__':
    xs = np.array([4, 10 , 16,20,25, 30,37, 43,46,55, 60 ])
    y1s = np.array([0.065, 0.082, 0.095,0.103 ,0.11, 0.13 ,0.16, 0.17,0.21, 0.24,0.3])
    plot_double_lines(len(xs), xs, y1s, 'Visualization of Linking Prediction')





