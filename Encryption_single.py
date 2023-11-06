from osgeo import ogr
import os

'''Read vector data (shp)'''


def Read_XYPo_fromshp(ori_shp):
    ds = ogr.Open(ori_shp, 0)
    layer = ds.GetLayer(0)
    feature_num = layer.GetFeatureCount()
    XLst, YLst, PoLst, X_sum, Y_sum = [], [], [], [], []
    for in_feature in layer:
        geom = in_feature.geometry()
        wkt = geom.ExportToWkt()
        pointstring = wkt[wkt.find('(') + 1:wkt.rfind(')')].split(',')
        x, y, po = [], [], []
        for point_value in pointstring:
            xy = point_value.split(' ')
            x += [float(xy[0])]
            y += [float(xy[1])]
            po += [(float(xy[0]), float(xy[1]))]
        X_sum += x  # 总的X坐标集合
        Y_sum += y
        XLst.append(x), YLst.append(y), PoLst.append(po)
    ds.Destroy()
    return XLst, YLst, PoLst, feature_num, X_sum, Y_sum


'''写出矢量数据'''


def Write_XYPo_toshp(ori_shp, en_shp, XLst_emb, YLst_emb):
    ds = ogr.Open(ori_shp, 0)
    in_layer = ds.GetLayer(0)
    feature_num = in_layer.GetFeatureCount()
    driver = ogr.GetDriverByName('ESRI Shapefile')
    data_source = driver.CreateDataSource(en_shp)
    get_srs = in_layer.GetSpatialRef()
    out_layer = data_source.CreateLayer(en_shp, get_srs, ogr.wkbLineString)
    out_layer.CreateFields(in_layer.schema)
    out_defn = out_layer.GetLayerDefn()
    if os.access(en_shp, os.F_OK):
        driver.DeleteDataSource(en_shp)
    feat_count = 0
    for in_feature in in_layer:
        geom = in_feature.geometry()
        wkt = geom.ExportToWkt()
        pointstring = wkt[wkt.find('(') + 1:wkt.rfind(')')].split(',')
        pts_new = ''
        point_num = 0
        for point_value in pointstring:
            xy = point_value.split(' ')
            x = float(xy[0])
            y = float(xy[1])
            en_x = XLst_emb[feat_count][point_num]
            en_y = YLst_emb[feat_count][point_num]
            pts_new += str(en_x) + ' ' + str(en_y) + ','
            point_num += 1
        en_wkt = wkt[0:wkt.find('(') + 1] + pts_new[:-1] + ')'
        out_feature = ogr.Feature(out_defn)
        en_Geometry = ogr.CreateGeometryFromWkt(en_wkt)
        out_feature.SetGeometry(en_Geometry)
        for i in range(1, in_feature.GetFieldCount()):
            value = in_feature.GetField(i)
            out_feature.SetField(i, value)
        out_layer.CreateFeature(out_feature)
        feat_count += 1
    ds.Destroy()


"""Scrambling based on Tent mapping"""


def Tent(feature_num, XList, YList, Xor, Yor, a, t0):
    for i in range(0, feature_num):
        X0 = Xor
        N = len(XList[i])
        Lx, RcLx = [], []

        for k in range(0, t0 + N):
            if X0 < 0.5:
                X0 = a * X0
            else:
                X0 = a * (1 - X0)
            Lx.append(X0)
        cLx = Lx[t0:]
        for j in cLx:
            xi = int(N * j) % N
            RcLx.append(xi)
        #  X坐标置乱
        for j in range(0, len(XList[i])):
            XList[i][j], XList[i][RcLx[j]] = XList[i][RcLx[j]], XList[i][j]
    RXLst = XList

    for m in range(0, feature_num):
        Y0 = Yor
        N = len(YList[m])
        Ly, RcLy = [], []
        for s in range(0, t0 + N):
            if Y0 < 0.5:
                Y0 = a * Y0
            else:
                Y0 = a * (1 - Y0)
            Ly.append(Y0)
        cLy = Ly[t0:]
        for n in cLy:
            yi = int(N * n) % N
            RcLy.append(yi)
        for n in range(0, len(YList[m])):
            YList[m][n], YList[m][RcLy[n]] = YList[m][RcLy[n]], YList[m][n]
    RYLst = YList

    return RXLst, RYLst


"""Scrambling based on PWLCM mapping"""


def PWLCM(feature_num, XList, YList, x0, B, t0):
    for i in range(0, feature_num):
        N = len(XList[i])
        xi = x0
        Li, RcLi = [], []
        # 混沌序列生成
        for s in range(0, t0 + N):
            if 0 <= xi < B:
                xi = xi / B
            elif B <= xi < 0.5:
                xi = (xi - B) / (0.5 - B)
            elif 0.5 <= xi < 1 - B:
                xi = (1 - B - xi) / (0.5 - B)
            else:
                xi = (1 - xi) / B
            Li.append(xi)
        cLi = Li[t0:]  # 舍去固定次数产生的迭代值
        # 向下取整
        for j in cLi:
            x = int(N * j) % N
            RcLi.append(x)  # 取整后的混沌序列
        for j in range(0, len(XList[i])):
            XList[i][j], XList[i][RcLi[j]] = XList[i][RcLi[j]], XList[i][j]
        for n in range(0, len(YList[i])):
            YList[i][n], YList[i][RcLi[n]] = YList[i][RcLi[n]], YList[i][n]
    return XList, YList


if __name__ == '__main__':
    fn_r = r"D:\RSA＿Encryption\实验结果图\En_waterways.shp"
    XLst, YLst, PLst, feature_num, X_sum, Y_sum = Read_XYPo_fromshp(fn_r)  # read vector data
    Xor, Yor = 0.45, 0.55  # 实验初始值
    a, t0 = 1.5, 1000  # 参数，t0为迭代次数
    x0, B, = 0.45, 0.25
    # RXLst, RYLst = Tent(feature_num, XLst, YLst, Xor, Yor, a, t0)
    RXLst2, RYLst2 = PWLCM(feature_num, XLst, YLst, x0, B, t0)
    fn_w = r"D:\RSA＿Encryption\实验结果图\PWLCM_waterways.shp"
    Write_XYPo_toshp(fn_r, fn_w, RXLst2, RYLst2)  # Write out the encrypted vector data
    print("finish")
