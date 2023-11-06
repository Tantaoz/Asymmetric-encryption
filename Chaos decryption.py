from Read_Write import *

"""Scramble decryption"""


def Tent(feature_num, XList, x0, a, t0):
    for i in range(0, feature_num):
        N = len(XList[i])
        xi = x0
        Li, RcLi = [], []
        # 混沌序列生成
        for k in range(0, t0 + N):
            if xi < 0.5:
                xi = a * xi
            else:
                xi = a * (1 - xi)
            Li.append(xi)
        cLi = Li[t0:]  # 舍去固定次数产生的迭代值
        for j in cLi:
            x = int(N * j) % N
            RcLi.append(x)
        #  coordinate decryption
        r = 1
        for j in reversed(RcLi):
            XList[i][j], XList[i][N - r] = XList[i][N - r], XList[i][j]
            r += 1
    return XList


if __name__ == '__main__':
    fn_r = r"E:\硕士\小论文\第三篇论文代码和实验\MAP\Team.shp"
    XLst, YLst, feature_num = Read_Shapfile(fn_r)  # Read the vector data to be decrypted
    x0, y0 = 0.45, 0.55  # 实验初始值
    a, b, t0 = 1.5, 1.25, 20  # 参数，t0为迭代次数
    XList, YList = Tent(feature_num, XLst, x0, a, t0), Tent(feature_num, YLst, y0, b, t0)
    fn_w = r"E:\硕士\小论文\第三篇论文代码和实验\MAP\DeTeam.shp"
    write_encrytpion_shp(fn_r, fn_w, XList, YList)  # Write out the decrypted vector data
    print("finish")
