import xuan


def zhu(xuanzhi, seed, **kwargs):

    """
    画竹子。
    :param xuanzhi: 宣纸纹理
    :param seed: 种子。整数列。每个数字应该在0~15之间
    """

    frame = 0        # 做视频用的帧

    pointer = 0                         # 从整数列的第0个读起

    h, w = xuanzhi.shape

    # 确定画几根竹子，每根竹子的位置，倾斜方向, 弯曲程度, 竹节长度，下笔粗细

    zhu_n = seed[pointer] % 3 + 1
    pointer += 1
    zhus, ultilized = [], []
    for i in range(zhu_n):
        while seed[pointer] in ultilized:
            pointer += 1
        wid = int(20 + xuan.np.sqrt(seed[pointer + 4]) * (-1) ** (seed[pointer + 4] // 3))
        zhus.append([int((seed[pointer] + 1) / 17 * w),  # 位置横坐标
                     h - 30 + seed[pointer + 5],  # 位置纵坐标
                     (xuan.np.sqrt(seed[pointer + 1]) * 4 + xuan.np.sqrt(seed[pointer + 2]) * 0.4) * (-1) ** (seed[pointer + 2] // 2),  # 倾斜方向
                     xuan.np.sqrt(seed[pointer + 3]) / 20 * (-1) ** (seed[pointer + 2] // 2),  # 弯曲程度
                     80 + wid / 2 + seed[pointer + 5] / 4,  # 竹节长度
                     wid,  # 下笔粗细
                     True])
        ultilized.append(seed[pointer])
        pointer += 6

    # 画主干

    j, sqt = 1, 0
    youjie = False        # 储存是否应当画竹节
    jies = []             # 储存可画竹节的位置
    zhu_k = zhu_n
    while zhu_k:
        # print(zhu_k)
        # print(zhus)
        for i in range(zhu_n):
            if not zhus[i][6]:
                continue
            print('第', j, '次迭代，创作主干中……    ', i, '/', zhu_k)
            my_maobi=xuan.maobi(radius=zhus[i][5], hair=0.6, noise=0.1)
            my_path=xuan.zhugan_stroke(start_x=zhus[i][0], start_y=zhus[i][1],     # 竹节起始点
                                        l=zhus[i][4], dir=zhus[i][2], c=0.3)
            xuanzhi, frame = my_maobi.paint(xuanzhi, path=my_path, fps=50, randpath=0.03, randpara=0.03, frame=frame, seqindice=(pointer-12, pointer+4))
            if youjie:
                jies.append([zhus[i][0], zhus[i][1], zhus[i][2]+90, zhus[i][5], sqt])
            sqt = xuan.np.sqrt(seed[pointer])
            zhus[i] = [int((zhus[i][4]+sqt*3+4)*xuan.np.sin(zhus[i][2]*11/630)+zhus[i][0]),              # 位置横坐标
                       int(-(zhus[i][4]+sqt*5+zhus[i][5]+4)*xuan.np.cos(zhus[i][2]*11/630)+zhus[i][1]),  # 位置纵坐标
                       zhus[i][2] + zhus[i][3] * seed[pointer] / 15,                                     # 倾斜方向
                       zhus[i][3],                                                                       # 弯曲程度
                       zhus[i][4] * (1 + seed[pointer + 1] / 100),                                       # 竹节长度
                       int(zhus[i][5] * (1 - seed[pointer + 2] / 160)),                                  # 笔刷粗细
                       zhus[i][6]]
            pointer += 3
        zhu_k = zhu_n
        youjie = True
        for i in zhus:
            if i[0]+i[4]*xuan.np.sin(i[2]*11/630) < 0 or i[0]+i[4]*xuan.np.sin(i[2]*11/630) > w or i[1]-i[4]*xuan.np.cos(i[2]*11/630) < 0 or i[5] < 4:
                i[6] = False
                zhu_k -= 1
        j += 1
        if j > 20:
            break

    # 画竹节
    zhis = []             # 储存画竹枝的位置

    print("创作竹节中……")
    for i in jies:
        adjust_l = i[3]*(1.6+seed[pointer+2]/80)          # 竹节长度，用来防止画出画布。很奇怪。
        if not(adjust_l<i[0]-i[3]/2<w-adjust_l and adjust_l<i[1]+i[3]*2/3+i[4]*2<h-adjust_l):
            continue
        my_maobi = xuan.maobi(radius=3+int(i[3]*seed[pointer]/80), hair=0.5+seed[pointer+1]/80, noise=0.2)
        my_path = xuan.zhujie_stroke(start_x=i[0]-i[3]/2,
                                     start_y=i[1]+i[3]*2/3 + i[4]*2,
                                     l=adjust_l, dir=i[2]+seed[pointer+3]/8, c=0.2)
        xuanzhi, frame = my_maobi.paint(xuanzhi, path=my_path, fps=50, randpath=0.03, randpara=0.03, frame=frame, seqindice=(pointer-12, pointer+4))
        zhis.append((i[0]-i[3]/2, i[1]+i[3]*2/3 + i[4]*2, 10, i[2], i[2]-80))
        zhis.append((i[0]+i[3]/2, i[1]+i[3]*2/3 + i[4]*2, 10, i[2]+260, i[2]+180))
        pointer += 4

    # 画竹枝

    print("创作竹枝中……")
    xuanzhi, d_p, zhuye_points, frame = zhu_branch(xuanzhi, seed[pointer:], range=zhis, w=w, h=h, decay2=0.2, frame=frame, indice=pointer)
    pointer += d_p

    print("创作竹叶中……")
    xuanzhi, frame = ye(xuanzhi, seed[pointer:], range=zhuye_points, w=w, h=h, frame=frame, indice=pointer)

    return xuanzhi


def branch(upper, lower, n, r, l, seed):

    """
    生成画竹枝和竹叶用的分布。
    :param upper: 上界
    :param lower: 下界
    :param n: 竹枝/竹叶数量
    :param r: 随机扩大的最大半径
    :param l: 平均长度
    :param seed: 随机数种子
    """

    pointer = 0
    res = []
    not_got_res = True
    while not_got_res:
        res = []
        for i in range(n):
            if pointer+2 >= len(seed):
                return res, 0
            res.append((seed[pointer]/15*(upper-lower)+lower,         # 竹枝/竹叶位置
                        seed[pointer+1]/80*r,                         # 扩大半径
                        (0.9+seed[pointer+2]/80)*l))                  # 长度
            pointer += 2
        not_got_res = False
        for i in range(n):
            for j in range(i+1, n):
                if res[i][0]-res[j][0] < (upper-lower)*0.12:
                    not_got_res = True
    return res, pointer


def zhu_branch(xuanzhi, seed, **kwargs):

    """
    画小的竹枝
    :param xuanzhi: 宣纸纹理
    :param seed: 随机数种子
    :param kwargs: 其他参数，如允许绘画的范围（以圆表示，（圆心x，圆心y，半径, 方位角1，方位角2））
    """

    decay = kwargs['decay'] if 'decay' in kwargs else 1                             # 下一枝还画的概率
    decay2 = kwargs['decay2'] if 'decay2' in kwargs else 0.2                        # 生成竹枝的概率
    z_range = kwargs['range'] if 'range' in kwargs else [(300, 500, 5, 0, 180)]     # 第一笔范围
    l = kwargs['l'] if 'l' in kwargs else 50                                        # 每根竹枝的平均长
    w = kwargs['w'] if 'w' in kwargs else 618                                       # 画布宽
    h = kwargs['h'] if 'h' in kwargs else 1000                                      # 画布高
    frame = kwargs['frame'] if 'frame' in kwargs else 0                             # 生成视频用的
    indice = kwargs['indice'] if 'indice' in kwargs else 0                          # 生成视频用的

    pointer = 0
    dec = decay2

    if z_range == []:
        return xuanzhi, pointer, []

    # 先选出一个，来保证至少会画出一个分支

    draw = [int((len(z_range) - 1) * seed[pointer] / 15)]  # 存放要画的分支之范围
    clear = False
    pointer += 1

    # 开始画
    my_maobi = xuan.maobi(radius=3, hair=0.5, noise=0.2)
    zhuye_point = []       # 存放绘制竹叶的位置

    while len(draw):

        if clear:
            draw = []
            dec = decay
            decay *= 0.82

        # 继续选别的

        for i in range(len(z_range)):
            if seed[pointer] / 16 < dec:
                if i not in draw:
                    draw.append(i)
            pointer += 1

        new_z_range = []
        for i in draw:

            # 用种子生成分支

            branching, d_p = [], 0
            if l*2<z_range[i][0]<w-l*2 and l*2<z_range[i][1]<h-l*2:
                branching, d_p = branch(z_range[i][4], z_range[i][3], seed[pointer]%3+1, z_range[i][3], l, seed[pointer+1:])
                pointer += 2

            if len(branching) and not clear:
                branching = [branching[0]]
            print(branching, not clear)

            pointer += d_p+1
            for j in branching:

                # 绘制分支

                sx = z_range[i][0]+j[1]*xuan.np.sin(j[0]*11/630)
                sy = z_range[i][1]-j[1]*xuan.np.cos(j[0]*11/630)
                zhuye_point.append((sx-7+seed[pointer+2], sy-7+seed[pointer+3], int(round(4+seed[pointer+4]/80)), 90, 270))
                my_zhuzhi = xuan.zhugan_stroke(l=j[2], dir=j[0],
                                               start_x=sx, start_y=sy,
                                               c=0.15+seed[pointer]/160,
                                               outstroke=1.4+seed[pointer+1]/80)
                pointer += 2
                xuanzhi, frame = my_maobi.paint(xuanzhi, path=my_zhuzhi, fps=50, randpath=0, randpara=0.03, frame=frame, seqindice=(pointer+indice-12, pointer+indice+4))

                # 计算新的分支

                if seed[pointer] / 16 < decay:
                    new_z_range.append((z_range[i][0]+(j[1]+j[2])*xuan.np.sin(j[0]*11/630),
                                        z_range[i][1]-(j[1]+j[2])*xuan.np.cos(j[0]*11/630),
                                        5, j[0]-40, j[0]+40))
                pointer += 1



        clear = True
        z_range = new_z_range
        print(z_range)

    return xuanzhi, pointer, zhuye_point, frame


def ye(xuanzhi, seed, **kwargs):

    """
    在指定的位置绘制竹叶。
    :param xuanzhi: 宣纸纹理
    :param seed: 随机数种子
    """

    z_range = kwargs['range'] if 'range' in kwargs else [(300, 500, 5, 70, 290)]   # 竹叶丛范围
    l = kwargs['l'] if 'l' in kwargs else 120                                      # 每片竹叶的平均长
    p = kwargs['p'] if 'p' in kwargs else 0.3                                      # 绘制一簇竹叶的概率
    w = kwargs['w'] if 'w' in kwargs else 618
    h = kwargs['h'] if 'h' in kwargs else 1000
    frame = kwargs['frame'] if 'frame' in kwargs else 0                            # 生成视频用的
    indice = kwargs['indice'] if 'indice' in kwargs else 0                         # 生成视频用的

    pointer = 0

    if z_range == []:
        return xuanzhi

    # 同样的逻辑，先选出一个。

    draw = [int((len(z_range) - 1) * seed[pointer] / 15)]
    pointer += 1

    # 选出其他的

    for i in range(len(z_range)):
        if seed[pointer]/15 < p:
            if i != draw[0]:
                draw.append(i)
        pointer += 1

    # 把选出来的画出来

    my_maobi = xuan.maobi(radius=13, hair=0.6, noise=0)
    for i in draw:
        branching, d_p = branch(z_range[i][4], z_range[i][3], seed[pointer]%3+2, 240*(1+seed[pointer]/15), l, seed[pointer+1:])
        pointer += d_p+1
        for j in branching:
            if not (0<z_range[i][0]+(j[1]+l*1.5)*xuan.np.sin(j[0]*11/630)<w and 0<z_range[i][1]-(j[1]+l*1.5)*xuan.np.cos(j[0]*11/630)<h):
                continue
            my_zhuye = xuan.zhuye_stroke(root_x=z_range[i][0]+j[1]*xuan.np.sin(j[0]*11/630),
                                         root_y=z_range[i][1]-j[1]*xuan.np.cos(j[0]*11/630),
                                         dir=j[0], l=j[2],
                                         outstroke1=1.2*(1+seed[pointer]/15),
                                         outstroke2=2*(1+seed[pointer+1]/15))
            print(z_range[i][0]+j[1]*xuan.np.sin(j[0]*11/630),z_range[i][1]-j[1]*xuan.np.cos(j[0]*11/630),j[0])
            pointer += 2
            xuanzhi, frame = my_maobi.paint(xuanzhi, path=my_zhuye, fps=50, randpath=0.03, randpara=0.03, frame=frame, seqindice=(pointer+indice-12, pointer+indice+4))

    return xuanzhi, frame


if __name__ == '__main__':
    xuanzhi = xuan.xuanize(width=618, height=1000)

    import random

    num = []
    for i in range(100000):
        num.append(random.randint(0, 15))

    xuan.cv2.imwrite('try.jpg', zhu(xuanzhi, num)*256)
