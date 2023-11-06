from RSA_En import *


def power_mod(base, d, n):
    result = 1
    while d > 0:
        if d % 2 == 1:
            result = (result * base) % n
        base = (base * base) % n
        d //= 2
    return result


def DRSA(Xlist, Ylist, features, d, n):
    XLst, YLst = Xlist, Ylist
    for i in range(0, features):
        for j in range(0, len(Xlist[i])):
            float_xi = Xlist[i][j] % 1
            integer_xi = int(Xlist[i][j])
            xor = integer_xi % 10
            k1 = (integer_xi % 100 - xor) / 10
            En_xi = int(integer_xi/ 100)
            De_xi = power_mod(En_xi, d, n)
            if xor==0:
                XLst[i][j] = (De_xi + float_xi) * (10 ** k1)
            else:
                XLst[i][j] = -(De_xi + float_xi) * (10 ** k1)
    for i in range(0, features):
        for j in range(0, len(Ylist[i])):
            float_yi = Ylist[i][j] % 1
            integer_yi = int(Ylist[i][j])
            yor = integer_yi % 10
            k2 = (integer_yi % 100 - yor) / 10
            En_yi = int(integer_yi/ 100)
            De_yi = power_mod(En_yi, d, n)
            if yor==0:
                YLst[i][j] = (De_yi + float_yi) * (10 ** k2)
            else:
                YLst[i][j] = -(De_yi + float_yi) * (10 ** k2)
    return XLst, YLst


if __name__ == '__main__':
    # 选择两个质数p和q
    e, d, n = 579, 1419, 2227

    fn =r"E:\硕士\小论文\第三篇论文代码和实验\实验结果图\Polygon.shp"
    fw =r"E:\硕士\小论文\第三篇论文代码和实验\实验结果图\De_Polygon.shp"
    XList, YList, feature_num = Read_Shapfile(fn)  # 读取原始矢量数据
    XLst, YLst = DRSA(XList, YList, feature_num, d, n)
    write_encrytpion_shp(fn, fw, XLst, YLst)
    print("finish")
