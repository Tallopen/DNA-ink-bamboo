"""
这里存储有基于action的画笔路径预设。
"""

from .action import *


def kai_horizontal_stroke():

    """
    汉字中的长横，楷书
    建议参数：毛笔半径为8，毛0.8，fps为40
    :return: path
    """

    apath = path(linear_node(60, 90, 1, strength=0.5),
                 linear_node(25, 85, 2, strength=0.3),
                 linear_node(45, 95, 1, strength=1),
                 linear_node(200, 75, 1.5, strength=1),
                 linear_node(213, 80, 1, strength=0.6),
                 linear_node(155, 80, 1, strength=0.8))
    return apath


def cao_horizontal_stroke():

    """
    汉字中的长横，草书
    建议参数：毛笔半径为12，毛0.5，fps为40
    :return: path
    """

    apath = path(linear_node(45, 95, 1, strength=1, apexd=3, apexangle=285),
                 linear_node(200, 75, 1.5, strength=1, apexangle=285),
                 linear_node(213, 80, 1, strength=1, apexangle=250),
                 linear_node(140, 110, 1, strength=0.4, ink=0.2, apexd=1.5, apexangle=250))
    return apath


def cao_double_vertical_stroke():

    """
    汉字中的长横，草书
    建议参数：毛笔半径为12，毛0.5，fps为40
    :return: path
    """

    apath = path(linear_node(75, 65, 1, strength=1, apexd=1.3, apexangle=285),
                 linear_node(80, 105, 1.5, strength=1, apexangle=285),
                 linear_node(164, 58, 0.5, strength=0, apexangle=0),
                 linear_node(170, 50, 2, strength=1, apexd=1.8, apexangle=310),
                 linear_node(125, 150, 2, strength=0.7, ink=0.2, apexd=1.4, apexangle=190))
    return apath


def zhugan_stroke(**kwargs):

    """
    绘制竹杆的路径。可以适当调整参数。推荐笔的粗细不要超过25
    :return: path
    """

    start_x = kwargs['start_x'] if 'start_x' in kwargs else 100        # 绘制竹杆的起点横坐标
    start_y = kwargs['start_y'] if 'start_y' in kwargs else 300        # 绘制竹杆的起点纵坐标
    direction = kwargs['dir'] if 'dir' in kwargs else 0                # 绘制竹杆的方向(0~360°)
    length = kwargs['l'] if 'l' in kwargs else 100                     # 绘制竹杆的长度
    outstroke = kwargs['outstroke'] if 'outstroke' in kwargs else 1.2  # 竹节处竹竿突出的强度
    c_conc = kwargs['c'] if 'c' in kwargs else 0.3                     # 竹杆当中墨的浓度（0~1）
    strength = kwargs['strength'] if 'strength' in kwargs else 1       # 绘图力度

    direction_radian = direction*np.pi/180

    apath = path(linear_node(start_x, start_y, 0.2,
                             conc=np.sqrt(c_conc),
                             apexd=outstroke,
                             strength=0.75*strength,
                             apexangle=direction+100),
                 linear_node(start_x, start_y, 0.5,
                             conc=c_conc,
                             strength=strength,
                             apexd=outstroke/2,
                             apexangle=direction+90),
                 linear_node(start_x+length*np.sin(direction_radian)/2,
                             start_y-length*np.cos(direction_radian)/2,
                             0.5,
                             strength=strength, conc=c_conc, apexd=outstroke/3, apexangle=direction+90),
                 linear_node(start_x+length*np.sin(direction_radian),
                             start_y-length*np.cos(direction_radian),
                             0.2,
                             strength=strength, conc=c_conc, apexd=outstroke/2, apexangle=direction+90),
                 linear_node(start_x+length*np.sin(direction_radian),
                             start_y-length*np.cos(direction_radian),
                             0.2, conc=np.sqrt(c_conc), strength=0.75*strength, apexd=outstroke, apexangle=direction+80))

    return apath


def zhujie_stroke(**kwargs):

    """
    绘制竹节的路径。可以适当调整参数。
    :return: path
    """

    start_x = kwargs['start_x'] if 'start_x' in kwargs else 100        # 绘制竹节的起点横坐标
    start_y = kwargs['start_y'] if 'start_y' in kwargs else 200        # 绘制竹节的起点纵坐标
    direction = kwargs['dir'] if 'dir' in kwargs else 90               # 绘制竹节的方向(0~360°)
    length = kwargs['l'] if 'l' in kwargs else 40                      # 绘制竹节的长度
    outstroke = kwargs['outstroke'] if 'outstroke' in kwargs else 1.2  # 竹节头突出的强度
    c_conc = kwargs['c'] if 'c' in kwargs else 1                       # 墨的浓度（0~1）

    direction_radian = direction * np.pi / 180

    apath = path(linear_node(start_x, start_y, 0.1,
                             conc=c_conc,
                             apexd=outstroke,
                             apexangle=direction+10),
                 linear_node(start_x, start_y, 0.3,
                             conc=c_conc,
                             apexd=0,
                             apexangle=direction),
                 linear_node(start_x + length * np.sin(direction_radian) / 2,
                             start_y - length * np.cos(direction_radian) / 2,
                             0.3, strength=0.7, conc=c_conc),
                 linear_node(start_x + length * np.sin(direction_radian),
                             start_y - length * np.cos(direction_radian),
                             0.1, conc=c_conc, apexd=0, apexangle=direction+180),
                 linear_node(start_x + length * np.sin(direction_radian),
                             start_y - length * np.cos(direction_radian),
                             0.2, conc=c_conc, apexd=outstroke, apexangle=direction + 170))

    return apath


def zhuye_stroke(**kwargs):

    """
    绘制竹叶的路径。可以适当调整参数。
    :return: path
    """

    root_x = kwargs['root_x'] if 'root_x' in kwargs else 100                 # 竹叶绘制起点横坐标
    root_y = kwargs['root_y'] if 'root_y' in kwargs else 100                 # 竹叶绘制起点纵坐标
    direction = kwargs['dir'] if 'dir' in kwargs else 230                    # 绘制竹叶的方向(0~360°)
    outstroke1 = kwargs['outstroke1'] if 'outstroke1' in kwargs else 1.2     # 竹叶头突出的强度
    outstroke2 = kwargs['outstroke2'] if 'outstroke2' in kwargs else 2       # 竹叶尾突出的强度
    length = kwargs['l'] if 'l' in kwargs else 40                            # 竹叶的长度

    direction_radian = direction * np.pi / 180

    apath = path(linear_node(root_x, root_y, 1,
                             apexangle=direction+180,
                             apexd=outstroke1,
                             strength=0.6),
                 linear_node(root_x, root_y, 0.1,
                             apexangle=direction+180,
                             apexd=0),
                 linear_node(root_x+length*np.sin(direction_radian)*0.3,
                             root_y-length*np.cos(direction_radian)*0.3,
                             0.4,
                             apexangle=direction,
                             apexd=0),
                 linear_node(root_x+length*np.sin(direction_radian),
                             root_y-length*np.cos(direction_radian),
                             1,
                             strength=0.3,
                             apexangle=direction,
                             apexd=0),
                 linear_node(root_x+length*np.sin(direction_radian),
                             root_y-length*np.cos(direction_radian),
                             1,
                             strength=0.3,
                             apexangle=direction,
                             apexd=outstroke2))

    return apath
