import os
from osgeo import ogr
import sys
import time

'''读入矢量数据（shp）'''


def Read_Shapfile(fn_ori):
    ds = ogr.Open(fn_ori, 0)
    if ds is None:
        sys.exit("Could not open {0}.".format(fn_ori))
    layer = ds.GetLayer(0)
    feature_num = layer.GetFeatureCount(0)
    X_Lst, Y_Lst = [], []
    for i in range(0, feature_num):
        feature = layer.GetFeature(i)
        geometry = feature.GetGeometryRef()
        if geometry.GetGeometryName() == 'POLYGON':
            geometry = geometry.GetGeometryRef(0)
        x, y = [0] * geometry.GetPointCount(), [0] * geometry.GetPointCount()
        for j in range(geometry.GetPointCount()):
            x[j] = geometry.GetX(j)
            y[j] = geometry.GetY(j)
        X_Lst.append(x), Y_Lst.append(y)
    ds.Destroy()
    return X_Lst, Y_Lst, feature_num


'''写出矢量数据'''


def write_encrytpion_shp(ori_shp, outputfile, En_X, En_Y):
    ds = ogr.Open(ori_shp, 0)
    if ds is None:
        sys.exit('Could not open {0}.'.format(ori_shp))
    '''1.创建数据源'''
    driver = ogr.GetDriverByName("ESRI Shapefile")
    if os.access(outputfile, os.F_OK):
        driver.DeleteDataSource(outputfile)
    '''2.复制一个新的图层'''
    layer = ds.GetLayer(0)
    newds = driver.CreateDataSource(outputfile)
    pt_layer = newds.CopyLayer(layer, 'a')  # 第1个参数是OGR的Layer对象，第2个参数是要生成图层的名称。对于Shapefile来说，这个名称是没有用的，但必须给这个字符串赋变量值。
    newds.Destroy()
    nds = ogr.Open(outputfile, 1)
    nlayer = nds.GetLayer(0)
    for i in range(nlayer.GetFeatureCount(0)):
        feature = nlayer.GetFeature(i)
        # geometry = feature.GetGeometryRef().GetGeometryRef(0)
        geometry = feature.GetGeometryRef()
        if geometry.GetGeometryName() == 'POLYGON':
            geometry = geometry.GetGeometryRef(0)
        for k in range(geometry.GetPointCount()):
            geometry.SetPoint_2D(k, En_X[i][k], En_Y[i][k])
        nlayer.SetFeature(feature)
    nds.Destroy()


"""Scrambling based on PWLCM mapping"""


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
        # 向下取整
        for j in cLi:
            x = int(N * j) % N
            RcLi.append(x)  # 取整后的混沌序列
        for j in range(0, len(XList[i])):
            XList[i][j], XList[i][RcLi[j]] = XList[i][RcLi[j]], XList[i][j]
    return XList


if __name__ == '__main__':
    fn_r = r"E:\硕士\小论文\第三篇论文代码和实验\实验结果图\Line2.shp"
    XLst, YLst, feature_num = Read_Shapfile(fn_r)  # read vector data
    x0, y0 = 0.35, 0.65  # 实验初始值
    a, b, t0 = 1.45, 1.25, 10  # 参数，t0为迭代次数
    start = time.perf_counter()
    RXLst, RYLst = Tent(feature_num, XLst, x0, a, t0), Tent(feature_num, YLst, y0, b, t0)
    end = time.perf_counter()
    print(end - start)
    fn_w = r"E:\硕士\小论文\第三篇论文代码和实验\实验结果图\Polygon_CS2.shp"
    write_encrytpion_shp(fn_r, fn_w, RXLst, RYLst)  # Write out the encrypted vector data
    print("finish")
