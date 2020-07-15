"""
扫描目录记录文件信息

文件名称    后缀    存放位置    大小    

计算文件唯一性可以使用md5、sha1、sha2计算
SHA1比MD5提供更高的安全性

md5 为128位，遇到大文件计算会比较慢
sha1 产生160位哈希值
sha2 产生224、256、384或512位哈希值
"""

import zlib
import hashlib
import pathlib


def checksum_crc32(filename, chunksize=65536):
    """Compute the CRC-32 checksum of the contents of the given filename"""
    with open(filename, "rb") as f:
        checksum = 0
        while chunk := f.read(chunksize):
            checksum = zlib.crc32(chunk, checksum)
        return checksum


def checksum_md5(filename, chunksize=2**20):
    """Compute the MD5 checksum of the contents of the given filename
    Linux 下校验方式 $ md5sum <filename>
    """
    m = hashlib.md5()
    with open(filename, "rb") as f:
        while chunk := f.read(chunksize):
            m.update(chunk)
    return m.hexdigest()


def checksum_sha1():
    pass


if __name__ == "__main__":
    # print(checksum_md5(
    #     '/mnt/h/QQDownload/Emil.Gilels.Sviatoslav.Richter.Lorin.Maazel.-.[Tchaikovsky.Prokofiev.Bartók.Piano.Concertos.Disc.1].专辑.(flac).flac'))
    p = pathlib.Path("/mnt/e")  # 需要遍历目录
    a = list(p.glob("**/*"))  # 需要查找文件后缀
    print(len(a))
