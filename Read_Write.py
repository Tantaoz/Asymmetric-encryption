import os
from osgeo import ogr
import sys

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
def GetSum(XLst, YLst):
    X_sum, Y_sum = [], []
    for i in range(len(XLst)):
        for j in range(len(XLst[i])):
            X_sum.append(XLst[i][j])
    for m in range(len((YLst))):
        for n in range(len(YLst[m])):
            Y_sum.append(YLst[m][n])
    return X_sum, Y_sum

if __name__ == '__main__':
    # fn_r = r'D:\CEWcode\主要公路.shp'
    fn=r'E:\硕士\小论文\第三篇论文代码和实验\MAP\mongolia-latest-free.shp\gis_osm_pois_free_1.shp'
    # XLst, YLst,feature_num = Read_Shapfile(fn_r)  # 读取原始矢量数据
    XLst, YLst, feature_num1 = Read_Shapfile(fn)
    # fn_w = r'D:\Watermark_Experiment\Hrite.shp'
    # write_encrytpion_shp(fn_r, fn_w,  XLst, YLst)  # 写出嵌入水印后的矢量数据
    # print("finish")
    # X_sum1, Y_sum1 = GetSum(XLst1, YLst1)
    X_sum, Y_sum =GetSum(XLst, YLst)
    print(len(XLst))
    print(len(X_sum))
    # print(len(X_sum)/len(X_sum1))



