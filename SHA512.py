import hashlib
import operator


def sha512(data):
    # Calculate SHA256 hash value
    hash_object = hashlib.sha512(data.encode())
    hex_digest = hash_object.hexdigest()

    # Convert a hexadecimal string to a binary array
    binary_array, K, key = [], [], []
    for c in hex_digest:
        bits = bin(int(c, 16))[2:].zfill(4)
        binary_array.extend([int(b) for b in bits])
    S = [binary_array[i:i + 8] for i in range(0, len(binary_array), 8)]  # 512 bits divided into 64 groups
    for i in range(len(S)):
        ki = ''.join(list(map(str, S[i])))
        K.append(int(ki, 2))  # binary to decimal
    key = [K[j:j + 8] for j in range(0, len(K), 8)]  # 64 decimal integers are equally divided into 8 groups
    return binary_array, K, key


def parameter(Sum, K, key):
    d = (Sum * 512) % 63  # Compute the comparison bit index
    for i in range(0, len(key)):
        for j in range(0, len(key[i])):
            if key[i][j] >= K[d]:
                key[i][j] = 0
            else:
                key[i][j] = 1
    return key


def group(Key):
    K1, K2, K3, K4, K5, K6, K7, K8 = Key[0], Key[1], Key[2], Key[3], Key[4], Key[5], Key[6], Key[7]
    A, B, C, D, E = [], [], [], [], []
    X0, Y0, a, b = 0, 0, 0, 0
    for i in range(0, 8):
        A.append(operator.xor(K1[i], K2[i]))
        B.append(operator.xor(K3[i], K4[i]))
        C.append(operator.xor(K5[i], K6[i]))
        D.append(operator.xor(K7[i], K8[i]))
        E.append(operator.xor(K3[i], K4[i]))
    for j in range(8):
        X0 += int(A[7 - j]) * pow(2, j)
        Y0 += int(B[7 - j]) * pow(2, j)
        a += int(C[7 - j]) * pow(2, j)
        b += int(D[7 - j]) * pow(2, j)
    X0 = X0 / 256
    Y0 = Y0 / 256
    a = a / 256 + 1
    b = b / 256 + 1
    return X0, Y0, a, b


if __name__ == "__main__":
    data = "hellowo rld"
    binary_array, K, key = sha512(data)
    print(len(binary_array))
    print(binary_array)
    print(K)
    print(len(K))
    print(key)
    print(len(key))
    Sum = 10000
    key1 = parameter(Sum, K, key)
    X0, Y0, a, b = group(key1)
    print(X0, Y0, a, b)
