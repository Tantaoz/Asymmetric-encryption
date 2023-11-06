from Read_Write import *
import random
import time

# 求两个数的最大公约数
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


# 计算e在模phi意义下的乘法逆元d
def multiplicative_inverse(e, phi):
    d = 0
    x1 = 0
    x2 = 1
    y1 = 1
    temp_phi = phi

    while e > 0:
        # 辗转相除求gcd和乘法逆元
        temp1 = temp_phi // e
        temp2 = temp_phi - temp1 * e
        temp_phi = e
        e = temp2

        x = x2 - temp1 * x1
        y = d - temp1 * y1

        x2 = x1
        x1 = x
        d = y1
        y1 = y

    if temp_phi == 1:  # 如果e和phi互质，则返回d+phi
        return d + phi


# 生成RSA密钥对
def generate_keypair(p, q):
    n = p * q  # 计算n
    phi = (p - 1) * (q - 1)  # 计算phi

    # 选择一个随机整数e使得1 < e < phi且e与phi互质
    e = random.randrange(1, phi)
    g = gcd(e, phi)
    while g != 1:  # 如果e和phi不互质，重新选择e
        e = random.randrange(1, phi)
        g = gcd(e, phi)

    # 计算e的乘法逆元d
    d = multiplicative_inverse(e, phi)

    # 返回公钥和私钥
    return (e, n), (d, n)


def encrypt_integer(number, e, n):
    # 加密整数部分
    encrypted_number = (number ** e) % n
    return encrypted_number


def decrypt_integer(encrypted_number, d, n):
    # 解密整数部分
    decrypted_number = (encrypted_number ** d) % n
    return decrypted_number


def RSA(Xlist, Ylist, features, e, n):
    XLst, YLst = Xlist, Ylist
    for i in range(0, features):
        for j in range(0, len(Xlist[i])):
            if Xlist[i][j] < 0:
                xor = 1
            else:
                xor = 0
            integer_part = int(Xlist[i][j])
            digits_count = len(str(abs(integer_part)))
            k1 = digits_count - 3
            XLst[i][j] = XLst[i][j] / (10 ** k1)
            integer_Xi = abs(int(XLst[i][j]))
            flaot_Xi =abs(XLst[i][j]) % 1
            en_Xi = encrypt_integer(integer_Xi, e, n)
            XLst[i][j] = en_Xi * 100 + flaot_Xi + k1*10+xor

    for i in range(0, features):
        for j in range(0, len(Ylist[i])):
            if Ylist[i][j] < 0:
                yor=1
            else:
                yor=0
            integer_part1 = int(YLst[i][j])
            digits_count1 = len(str(abs(integer_part1)))
            k2 = digits_count1 - 3
            YLst[i][j] = YLst[i][j] / (10 ** k2)
            integer_Yi = abs(int(YLst[i][j]))
            flaot_Yi = abs(YLst[i][j]) % 1
            en_Yi = encrypt_integer(integer_Yi, e, n)
            YLst[i][j] = en_Yi * 100 + flaot_Yi + k2*10+yor
    return XLst, YLst


if __name__ == '__main__':
    # 选择两个质数p和q
    p = 131
    q = 19
    # 生成RSA密钥对
    public, private = generate_keypair(p, q)
    e, n = public[0], public[1]
    d = private[0]
    print(e, d, n)
    fn = r"E:\硕士\小论文\第三篇论文代码和实验\MAP\Line.shp"
    fw = r"E:\硕士\小论文\第三篇论文代码和实验\实验结果图\Point2.shp"
    XList, YList, feature_num = Read_Shapfile(fn)  # 读取原始矢量数据
    start = time.perf_counter()
    XLst, YLst = RSA(XList, YList, feature_num, e, n)
    end = time.perf_counter()
    print(end - start)
    # write_encrytpion_shp(fn, fw, XLst, YLst)
    print("finish")
    # print("公钥: ", public)
    # print("私钥: ", private)
    # number=458
    # encrypted_number = encrypt_integer(number, e, n)
    # decrypted_number = decrypt_integer(encrypted_number, d, n)
    #
    # print("原始整数：", number)
    # print("加密后：", encrypted_number)
    # print("解密后：", decrypted_number)
