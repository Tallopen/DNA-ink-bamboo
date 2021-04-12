import numpy as np


class node:

    def __init__(self, position_x, position_y, delta_t, **kwargs):

        """
        建立作为关键帧的节点，用于通过插值描述出毛笔的运动路径、力度变化等
        :param position_x: 落笔位置横坐标（以左上为原点，向右横坐标增大，向下纵坐标增大）
        :param position_y: 落笔位置纵坐标
        :param delta_t: 在插值节点序列中，距上一个节点的时间，默认为单位时间1
        """

        assert delta_t >= 0, 'parameter delta_t should be 0 or positive; got ' + str(delta_t)

        self.position_x = position_x         # 落笔位置，横坐标
        self.position_y = position_y         # 落笔位置，纵坐标
        self.delta_t = delta_t               # 距上一个节点的时间

        self.apex_a = kwargs['apexangle'] if 'apexangle' in kwargs else 0        # 笔锋偏移角度，0~360°
        self.apex_d = kwargs['apexd'] if 'apexd' in kwargs else 0                # 笔锋偏移量
        self.conc = kwargs['conc'] if 'conc' in kwargs else 1                    # 墨浓度（0~1）
        self.ink = kwargs['ink'] if 'ink' in kwargs else 1                       # 蘸墨量（0~1）
        self.offset_d = kwargs['offsetd'] if 'offsetd' in kwargs else 0          # 落笔重心偏移量（0~1）
        self.offset_a = kwargs['offsetangle'] if 'offsetangle' in kwargs else 0  # 落笔重心偏移角度，0~360°
        self.retain = kwargs['strength'] if 'strength' in kwargs else 1          # 落笔力度（0~1）


class linear_node(node):

    """
    插值算法设置为线性的节点
    """

    def __init__(self, position_x, position_y, delta_t=1, **kwargs):

        super().__init__(position_x, position_y, delta_t, **kwargs)

        self.time_weight = kwargs['tweight'] if 'tweight' in kwargs else 1      # 设置时间插值的权重，值越大笔在此处走得越慢

    def __add__(self, other):

        """
        定义节点之间的加法，即所有属性值的加和
        :param other: 另一个节点
        """

        if type(other) == linear_node:

            return linear_node(self.position_x + other.position_x,
                               self.position_y + other.position_y,
                               0,
                               apexangle=self.apex_a + other.apex_a,
                               apexd=self.apex_d + other.apex_d,
                               conc=self.conc + other.conc,
                               ink=self.ink + other.ink,
                               offsetangle=self.offset_a + other.offset_a,
                               offsetd=self.offset_d + other.offset_d,
                               strength=self.retain + other.retain,
                               tweight=0)

        else:

            return linear_node(self.position_x + other[0],
                               self.position_y + other[1],
                               0,
                               apexangle=self.apex_a + other[3],
                               apexd=self.apex_d + other[4],
                               conc=self.conc + other[5],
                               ink=self.ink + other[6],
                               offsetangle=self.offset_a + other[7],
                               offsetd=self.offset_d + other[8],
                               strength=self.retain + other[9],
                               tweight=0)

    def __mul__(self, other):

        """
        定义节点与数字的乘法，即所有属性值去乘以这个数字
        :param other: 一个数字
        """

        if type(other) in (int, float):

            return linear_node(self.position_x *other,
                               self.position_y *other,
                               0,
                               apexangle=self.apex_a *other,
                               apexd=self.apex_d *other,
                               conc=self.conc *other,
                               ink=self.ink *other,
                               offsetangle=self.offset_a *other,
                               offsetd=self.offset_d *other,
                               strength=self.retain *other,
                               tweight=0)

        else:

            return linear_node(self.position_x * other[0],
                               self.position_y * other[1],
                               0,
                               apexangle=self.apex_a * other[3],
                               apexd=self.apex_d * other[4],
                               conc=self.conc * other[5],
                               ink=self.ink * other[6],
                               offsetangle=self.offset_a * other[7],
                               offsetd=self.offset_d * other[8],
                               strength=self.retain * other[9],
                               tweight=0)

    def __rmul__(self, other):

        return self*other

    def __truediv__(self, other):

        """
        节点与数字的除法，所有属性值去除以这个数字
        """

        return self *(1/other)


class path:

    """
    定义走笔的路径
    """

    def __init__(self, *nodes):

        """
        建立一条路径，向其中添加节点
        :param nodes: 需要加入的节点，一个或多个，应当按照时间顺序排好
        """

        self.nodes = []            # 存放路径节点

        for i in nodes:
            if type(i) in (linear_node,):
                self.nodes.append(i)

    def append(self, *nodes):

        """
        在路径的最后继续插入节点
        :param nodes: 需要添加的节点，一个或多个
        """

        for i in nodes:
            if type(i) in (linear_node,):
                self.nodes.append(i)

    def make(self, **kwargs):

        """
        将路径解释为多个帧，当maobi类调用时，用毛笔笔刷描帧
        :param kwargs: 控制参数
        """

        fps = kwargs['fps'] if 'fps' in kwargs else 25                    # 每单位时间描的帧数
        random_path = kwargs['randpath'] if 'randpath' in kwargs else 0   # 为路径叠加噪声的强度
        random_para = kwargs['randpara'] if 'randpara' in kwargs else 0   # 为参数叠加噪声的强度（0~1）

        # 插帧

        frames = []
        for i in range(len(self.nodes ) -1):
            lena = 2*self.nodes[i].time_weight / (self.nodes[i].time_weight + self.nodes[i + 1].time_weight)
            frame_n = round(self.nodes[i].delta_t * fps)
            if frame_n == 0:
                frame_n = 1
            for j in range(1, frame_n + 1):

                # 确定帧
                if lena == 1:
                    check_point = j / frame_n
                else:
                    check_point = (np.sqrt(lena ** 2 + 4 * j / frame_n * (1 - lena)) - lena) / 2 / (1 - lena)
                new_frame = self.nodes[i] * (1 - check_point) + self.nodes[i + 1] * check_point

                # 添加噪声
                new_frame *= np.hstack(([1, 1, 0],
                                        np.random.random(3) * random_para * 2 + np.ones(3) * (1 - random_para),
                                        np.random.random(4) * random_para + np.ones(4) * (1 - random_para)))
                new_frame += np.hstack((np.random.random(2) * random_path * 2 + np.ones(2) * (1 - random_path),
                                        [0, 0, 0, 0, 0, 0, 0, 0]))

                # 冲淡墨迹
                new_frame.conc = 1 / fps - 1 / fps * (1 - new_frame.conc)

                if new_frame.position_x > 0 and new_frame.position_y > 0:
                    frames.append(new_frame)

        return frames


