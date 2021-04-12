"""
无特殊说明，代码中所有角度均指方位角，即以正上方为0度，顺时针旋转方向度数增加
"""

SEQ = "AGAGTTTGATCCTGGCTCAGGACGAACGCTGGCGGCGTGCCTAATACATGCAAGTCGAGCGGACAGATGGGAGCTTGCTCCCTGATGTTAGCGGCGGACGGGTGAGTAACACGTGGGTAACCTGCCTGTAAGACTGGGATAACTCCGGGAAACCGGGGCTAATACCGGATGGTTGTTTGAACCGCATGGTTCAAACATAAAAGGTGGCTTCGGCTACCACTTACAGATGGACCCGCGGCGCATTAGCTAGTTGGTGAGGTAACGGCTCACCAAGGCAACGATGCGTAGCCGACCTGAGAGGGTGATCGGCCACACTGGGACTGAGACACGGCCCAGACTCCTACGGGAGGCAGCAGTAGGGAATCTTCCGCAATGGACGAAAGTCTGACGGAGCAACGCCGCGTGAGTGATGAAGGTTTTCGGATCGTAAAGCTCTGTTGTTAGGGAAGAACAAGTACCGTTCGAATAGGGCGGTACCTTGACGGTACCTAACCAGAAAGCCACGGCTAACTACGTGCCAGCAGCCGCGGTAATACGTAGGTGGCAAGCGTTGTCCGGAATTATTGGGCGTAAAGGGCTCGCAGGCGGTTTCTTAAGTCTGATGTGAAAGCCCCCGGCTCAACCGGGGAGGGTCATTGGAAACTGGGGAACTTGAGTGCAGAAGAGGAGAGTGGAATTCCACGTGTAGCGGTGAAATGCGTAGAGATGTGGAGGAACACCAGTGGCGAAGGCGACTCTCTGGTCTGTAACTGACGCTGAGGAGCGAAAGCGTGGGGAGCGAACAGGATTAGATACCCTGGTAGTCCACGCCGTAAACGATGAGTGCTAAGTGTTAGGGGGTTTCCGCCCCTTAGTGCTGCAGCTAACGCATTAAGCACTCCGCCTGGGGAGTACGGTCGCAAGACTGAAACTCAAAGGAATTGACGGGGGCCCGCACAAGCGGTGGAGCATGTGGTTTAATTCGAAGCAACGCGAAGAACCTTACCAGGTCTTGACATCCTCTGACAATTCTAGAGATAGGACGTCCCCTTCGGGGGCAGAGTGACAGGTGGTGCATGGTTGTCGTCAGCTCGTGTCGTGAGATGTTGGGTTAAGTCCCGCAACGAGCGCAACCCTTGATCTTAGTTGCCAGCATTCAGTTGGGCACTCTAAGGTGACTGCCGGTGACAAACCGGAGGAAGGTGGGGATGACGTCAAATCATCATGCCCCTTATGACCTGGGCTACACACGTGCTACAATGGACAGAACAAAGGGCAGCGAAACCGCGAGGTTAAGCCAATCCCACAAATCTGTTCTCAGTTCGGATCGCAGTCTGCAACTCGACTGCGTGAAGCTGGAATCGCTAGTAATCGCGGATCAGCATGCCGCGGTGAATACGTTCCCGGGCCTTGTACACACCGCCCGTCACACCACGAGAGTTTGTAACACCCGAAGTCGGTGAGGTAACCTTTTAGGAGCCAGCCGCCGAAGGTGGGACAGATGATTGGGGTGAAGTCGTAACAAGGTAGCCGTATCGGAAGGTGCGGCTGGATCACCT"*100

import cv2
import random
from src import *


# 宣纸参数，噪波方向（左右，上下）

XUAN_DIR_WE = 0
XUAN_DIR_NS = 1

# 宣纸参数，非噪波方向（左上右下，左下右上）

XUAN_DIR_NW_SE = 2
XUAN_DIR_NE_SW = 3


def xuanize(width=1000, height=618, **kwargs):

    """
    生成宣纸纹理，以np.array的格式表示
    :param width: 宣纸宽
    :param height: 宣纸高
    :return: np.array (0~1之间)
    """

    per_1 = kwargs['per1'] if 'per1' in kwargs else 4           # 噪波周期
    per_2 = kwargs['per2'] if 'per2' in kwargs else 4           # 非噪波周期
    peak = kwargs['peak'] if 'peak' in kwargs else 1.5          # 噪波波峰高度
    decay1 = kwargs['decay1'] if 'decay1' in kwargs else 0.03   # 噪波抹匀权重
    decay2 = kwargs['decay2'] if 'decay2' in kwargs else 0.03   # 非噪波抹匀权重
    dir_1 = kwargs['dir1'] if 'dir1' in kwargs else 0           # 噪波方向，横或纵
    dir_2 = kwargs['dir2'] if 'dir2' in kwargs else 2           # 非噪波方向，左上-右下或右上-左下

    # 生成噪音图像

    a = np.random.random((height, width))
    if dir_1 == XUAN_DIR_NS:
        A = np.linspace(0, height-1, height).reshape((height, 1))
    else:
        A = np.linspace(0, width-1, width).reshape((1, width))
    a *= peak/2*np.sin(A*2*np.pi/per_1)+peak/2
    a = cv2.threshold(a, 1.0, 1.0, cv2.THRESH_TRUNC)
    a = np.array(a)[1]

    # 生成非噪波周期性正弦图像

    b = np.zeros((height, width))
    if dir_2 == XUAN_DIR_NW_SE:
        for i in range(height):
            for j in range(width):
                b[i, j] = np.sin((i+j)*2*np.pi/per_2)*0.5+0.5
    else:
        for i in range(height):
            for j in range(width):
                b[i, j] = np.sin((i-j)*2*np.pi/per_2)*0.5+0.5

    # 生成空白

    c = np.ones((height, width))

    res = a*decay1+b*decay2+c*(1-decay1-decay2)
    # cv2.imwrite('video/0000_xuan.png', res*256)       # 生成视频，必要时注掉即可

    return res


class maobi:

    def __init__(self, **kwargs):

        """
        生成毛笔笔刷，以np.array表示每根笔毛的长度（0~1）
        """

        hair = kwargs['hair'] if 'hair' in kwargs else 0.8                 # “笔毛”密度
        radius = kwargs['radius'] if 'radius' in kwargs else 20            # “笔毛”分布半径
        noise = kwargs['noise'] if 'noise' in kwargs else 0.05             # “笔毛”分布噪声

        # 生成笔毛

        width = radius*2-1
        brush = np.random.random((width, width))*noise+1

        # 叠加表示笔毛长度的锥形分布

        for i in range(width):
            for j in range(width):
                brush[i,j] += np.sqrt((i-radius)**2+(j-radius)**2)/radius-hair
                brush[i,j] = 1 if brush[i,j] > 1 else 0 if brush[i,j] < 0 else brush[i,j]

        self.width = width        # 毛笔直径
        self.brush = brush        # 笔毛长度
        self.paint_brush = None   # 用于绘画的画笔笔刷

    def set(self, **kwargs):

        """
        生成画笔笔刷
        """

        apex_a = kwargs['apexangle'] if 'apexangle' in kwargs else 0            # 笔锋偏移角度，0~360°
        apex_d = kwargs['apexd'] if 'apexd' in kwargs else 0                    # 笔锋偏移量
        conc = kwargs['conc'] if 'conc' in kwargs else 1                        # 墨浓度（0~1）
        ink = kwargs['ink'] if 'ink' in kwargs else 1                           # 蘸墨量（0~1）
        offset_a = kwargs['offsetangle'] if 'offsetangle' in kwargs else 0      # 落笔重心偏移角度，0~360°
        offset_d = kwargs['offsetd'] if 'offsetd' in kwargs else 0              # 落笔重心偏移量（0~1）
        retain = kwargs['strength'] if 'strength' in kwargs else 1              # 落笔力度（0~1）

        # print(apex_a, apex_d, conc, ink, offset_a, offset_d, retain)

        apex_d *= self.width / 2
        apex_a *= np.pi/180

        # 根据“落笔力度”生成用于绘图的笔刷

        p_brush = np.ones((self.width, self.width))
        for i in range(self.width):
            for j in range(self.width):
                if self.brush[i, j] < retain:
                    p_brush[i, j] = 0
                else:
                    gotten = False
                    if i > 0:
                        if self.brush[i-1, j] < retain:
                            gotten = True
                    if i < self.width-1:
                        if self.brush[i+1, j] < retain:
                            gotten = True
                    if j > 0:
                        if self.brush[i, j-1] < retain:
                            gotten = True
                    if j < self.width-1:
                        if self.brush[i, j+1] < retain:
                            gotten = True
                    if gotten:
                        if random.random() < retain:
                            p_brush[i, j] = 0

        # 生成基于落笔重心偏移和蘸墨量的修改

        modif = np.ones((self.width, self.width))
        offset_d *= self.width
        offset_a *= np.pi/180
        for i in range(self.width):
            for j in range(self.width):
                modif[i,j] -= ((i-self.width//2+1+offset_d*np.cos(offset_a))**2+(j-self.width//2+1-offset_d*np.sin(offset_a))**2)**10/(self.width**20)
        modif *= ink

        # 根据蘸墨量再次修改笔刷

        np_brush = np.ones((self.width, self.width))
        for i in range(self.width):
            for j in range(self.width):
                if p_brush[i, j]:
                    gotten = False
                    if i > 0:
                        if p_brush[i-1, j] == 0:
                            gotten = True
                    if i < self.width-1:
                        if p_brush[i+1, j] == 0:
                            gotten = True
                    if j > 0:
                        if p_brush[i, j-1] == 0:
                            gotten = True
                    if j < self.width-1:
                        if p_brush[i, j+1] == 0:
                            gotten = True
                    if gotten:
                        if random.random() < modif[i, j]:
                            np_brush[i, j] = 0
                else:
                    if random.random() < modif[i, j]:
                        np_brush[i, j] = 0

        # 根据总偏移量计算变换距离

        radius = self.width // 2 + 1
        displacement = np.zeros((self.width, self.width))
        for i in range(self.width):
            for j in range(self.width):
                displacement[i, j] = apex_d-np.sqrt(apex_d**2/radius**2*((i-radius)**2+(j-radius)**2))
                if displacement[i, j] < 0:
                    displacement[i, j] = 0

        # 构建适合变换大小的笔刷

        new_width = int(round(self.width+apex_d*2))
        fp_brush = np.ones((new_width, new_width))

        # 考虑墨浓度，进行变换

        for i in range(self.width):
            for j in range(self.width):
                if np_brush[i,j] == 0:
                    for k in range(int(round(100*(1-retain))), 101):
                        fill_x = int(round(apex_d+i+displacement[i,j]*k/100*np.sin(apex_a)))
                        fill_y = int(round(apex_d+j-displacement[i,j]*k/100*np.cos(apex_a)))
                        fp_brush[fill_y, fill_x] *= (1-conc)

        self.paint_brush = fp_brush

    def __gnode(self, anode):

        """
        从节点修改画笔状态
        :param anode: 某个节点
        """

        assert type(anode) in (node, linear_node), 'unsupported data: not a node'

        self.set(apexangle=anode.apex_a,
                 apexd=anode.apex_d,
                 conc=anode.conc,
                 ink=anode.ink,
                 offsetangle=anode.offset_a,
                 offsetd=anode.offset_d,
                 strength=anode.retain)

    def paint(self, xuanzhi, **kwargs):

        """
        在宣纸纹理上留下笔刷痕迹。
        :param xuanzhi: 宣纸
        """

        # 参数调整

        position_x = kwargs['x'] if 'x' in kwargs else 0
        position_y = kwargs['y'] if 'y' in kwargs else 0
        nnn = kwargs['frame'] if 'frame' in kwargs else 0
        seq_index = kwargs['seqindice'] if 'seqindice' in kwargs else (0, 10)

        # 绘制
        if 'anode' in kwargs:
            path = [kwargs['anode']]
        elif 'path' in kwargs:
            path = kwargs['path'].make(**kwargs)
        else:
            path = [None]
        for nodes in path:
            if nodes is not None:
                self.__gnode(nodes)
                position_x = int(round(nodes.position_x))
                position_y = int(round(nodes.position_y))
            size = self.paint_brush.shape[0]
            radius_m = size // 2 + 1
            temp_xuanzhi = np.ones((xuanzhi.shape[0]+radius_m*2,xuanzhi.shape[1]+radius_m*2))
            temp_xuanzhi[radius_m:xuanzhi.shape[0]+radius_m, radius_m:xuanzhi.shape[1]+radius_m] = xuanzhi
            temp_xuanzhi[position_y:position_y+size, position_x:position_x+size] *= self.paint_brush
            xuanzhi = temp_xuanzhi[radius_m:xuanzhi.shape[0]+radius_m, radius_m:xuanzhi.shape[1]+radius_m]

            # 生成视频，必要时注掉就可以
            # nnn += 1
            # img = cv2.putText(xuanzhi*256, SEQ[max(0, seq_index[0]*2-2):seq_index[1]*2+6], (40, 960), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 0, 2)
            # cv2.imwrite('video/'+str(nnn).rjust(4, '0')+'_xuan.png', img)

        return xuanzhi, nnn


if __name__ == '__main__':

    # 绘制

    my_xuanzhi = xuanize(dir1=XUAN_DIR_NS, dir2=XUAN_DIR_NE_SW)
    my_path1 = zhugan_stroke(l=120, dir=40, c=0.15, outstroke=1.5)
    my_maobi1 = maobi(radius=4, hair=0.6, noise=0)
    my_xuanzhi = my_maobi1.paint(my_xuanzhi, path=my_path1, fps=50, randpath=0, randpara=0.03)

    # 显示

    cv2.imshow('try!', my_xuanzhi)
    cv2.waitKey(0)
