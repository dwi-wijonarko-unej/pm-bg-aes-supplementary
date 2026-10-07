"""Verbatim-logic reference of canonical notebook cell 1 (ori ``7495Mw2mNX3t``).

Only adaptations: operates on bytes (no ``fromfile``/Colab), and
``aes_encrypt`` accepts an injected ``iv`` used SOLELY by the test harness
to make ciphertext deterministic (production default stays random via
``iv=None``). Transform code is otherwise character-faithful to the source.
"""

import hashlib

import numpy as np
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


def hitung_entropy(data):
    hist = np.bincount(data, minlength=256)
    prob = hist / np.sum(hist)
    entropy = -np.sum([p * np.log2(p) for p in prob if p > 0])
    return entropy


def pilih_matriks_ai(data):
    filesize = len(data)
    entropy = hitung_entropy(data)
    if filesize < 50000:
        n = 4 if entropy < 5 else 6
    elif filesize < 500000:
        n = 8 if entropy < 6 else 12
    elif filesize < 5000000:
        n = 16 if entropy < 7 else 24
    else:
        n = 32 if entropy < 7.5 else 48
    return n


def kunci_permutasi(p, q, ed='e'):
    n = p + q
    P = np.eye(n, dtype=np.int32)
    perm = list(range(n))
    if q >= 2:
        perm[p], perm[p+1] = perm[p+1], perm[p]
    if q >= 4:
        perm[p+2], perm[p+3] = perm[p+3], perm[p+2]
    P = P[perm, :]
    if ed == 'e':
        return P, 0
    elif ed == 'd':
        return P, P.T


def aes_encrypt(pesan, kunci, iv=None):
    data = bytes(pesan)
    key = hashlib.sha256(kunci.encode()).digest()
    cipher = AES.new(key, AES.MODE_CBC, iv=iv) if iv else AES.new(key, AES.MODE_CBC)
    iv_out = cipher.iv
    padded_data = pad(data, AES.block_size)
    ciphertext = cipher.encrypt(padded_data)
    return list(iv_out + ciphertext)


def aes_decrypt(data, kunci):
    key = hashlib.sha256(kunci.encode()).digest()
    data = bytes(data)
    iv = data[:AES.block_size]
    ciphertext = data[AES.block_size:]
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    decrypted_padded = cipher.decrypt(ciphertext)
    decrypted = unpad(decrypted_padded, AES.block_size)
    return list(decrypted)


def enkripsi_bytes(mp, password2, iv=None):
    """Notebook ``enkripsi`` on a uint8 array; returns (blob, n, len_hill)."""
    n = pilih_matriks_ai(mp)
    p, q = n//2, n - n//2
    x0_str = "0." + str(password2) + "1"
    len_shift = mp.size % n
    len_hill = mp.size - len_shift
    kunciku, _ = kunci_permutasi(p, q, 'e')
    mp_reshape = mp[:len_hill].reshape((n, int(len_hill / n))) if len_hill else np.empty((n, 0), dtype=np.uint8)
    m_kali = np.dot(kunciku.astype(np.int32), mp_reshape.astype(np.int32)) % 256
    m_kali = m_kali.astype(np.uint8)
    maes = aes_encrypt(mp[len_hill:], x0_str, iv=iv)
    m_kali_1d = m_kali.reshape(len_hill)
    header_n = np.array(list(n.to_bytes(4, byteorder='big')), dtype=np.uint8)
    header_len = np.array(list(len_hill.to_bytes(8, byteorder='big')), dtype=np.uint8)
    return np.concatenate((header_n, header_len, m_kali_1d, np.array(maes, dtype=np.uint8))), n, len_hill


def dekripsi_bytes(mc, password2):
    """Notebook ``dekripsi`` on a uint8 array; returns recovered array."""
    n = int.from_bytes(bytes(mc[:4]), byteorder='big')
    len_hill = int.from_bytes(bytes(mc[4:12]), byteorder='big')
    hill_part = mc[12:12 + len_hill]
    aes_part = mc[12 + len_hill:]
    p, q = n//2, n - n//2
    x0_str = "0." + str(password2) + "1"
    _, balikku = kunci_permutasi(p, q, 'd')
    mc_reshape = hill_part.reshape((n, int(len_hill / n))) if len_hill else np.empty((n, 0), dtype=np.uint8)
    m_kali = np.dot(balikku.astype(np.int32), mc_reshape.astype(np.int32)) % 256
    m_kali = m_kali.astype(np.uint8)
    maes = aes_decrypt(aes_part.tolist(), x0_str)
    m_kali_1d = m_kali.reshape(len_hill)
    return np.concatenate((m_kali_1d, np.array(maes, dtype=np.uint8)))
