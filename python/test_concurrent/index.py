## the dataset for testing: http://corpus-texmex.irisa.fr/
## download sift.tar.gz, copy it to folder: python/test_concurrent/bigann/
## and decompress the file: tar zxvf sift.tar.gz

import numpy as np
import requests
import base64
import json
import argparse

from data import *

QUERY1 = "失败 1bKlPnGT4b4w2O09IVjVvNwunD6itj0+yo2ivNdo0T4Wbnk7JNUnPpdvvT0naxQ+1IBhPjtzzz1cAhA+zZFFvi4Dzj15kXm+odn1vaTGJL79ogQ9DcSCPmDkxb2MSBQ+UpqtPmWmBD7VzJq9sU1Kviv7Jj+M9II+SDVsvApIu70aMwk9hbGFOyfaZT7L8iU+z/eTveyKWT65qfG+cuFQPvAVXbz0UYa9QGm4PmN/Gb30bly+jIE1vcvWwr6Nfgi/PWJ0PA71uz2qYwW+rad2Ps5SMr+6gpU+9fbHPfHYT7z0TZo9oinbPULt5z6SPcI8YvXPPhHIVT5cHFU+SmKpvr9Fv74qN9G82PRwvnh/nD793Tu97Sjmvn7//r4EcNM9A3sMvfJ6MD4Kup2+g8NLvQJm5j5beck9Q+L+PcjSB7z7HnU8dA27Pj82Sbw4aRo+uVD5Pg3FnTwnMjO+ZOWXPGFuG7/JV9q+0zNNvnrerb2eCIq+e8GnvCDt/z2RtpE9AhESPgQ6kz0HPzG//fjrvc5vGLsMA3Y+Zamtvs4X+zzpKUI+I90PPcpskLyPNVO+C9XNvJmCtbz5L9A9/YJtvk8DBr1PBOG+BtSLPhDrDTwFa7y9qgqNvKJ8QT7IQC4+D0dHvq5+LL4jTRy+6srnPrNFUj6FlxA+qwYJv1/Tc76POT++YqMsvEzgtj0yPuy9saWnvdwt8b7tvF2+AWiUvQLZi74Lexq+5zYhvdh/Hb4Fazy+1CrqvjHti74FapE+6rLYvTBL270X9P49OdblPbeZWj718dA9UkgSvny0SD5Epdm+PiPRvWZrDb65AHS+G9mVvfPiVL6vlIW+nfMTvcTuBz/yzTa9orOsPQAAcD7kLkK9fcscPuAO9L08aDY+YhFzPiBhmDxuNes9kC9hvd/8Rj6Y3rY+R3PEPZI7bL0jSfC9o0C/PZ1HRb3/H6c9iDC2vl1SJb5aZqG+c7lRPiHOE75U/Zo+/7PGvV2ozD5L5Y29h2s1PLIRiD43woK+e/fvPv8IQzx7oJU9XW6wPsBci7zsbVO+dNA1vmMLoT0="
QUERY2 = "成功 XhMSvQlOTb6rzX+9fAr4PpErtT2hvxA94lxjPghyED4730+97PekPcqKAT7PgWU+hCzLPXIYTL1jKSK+iZgCvqirOz7erIG+8kDkvhEerb2VYnc+A5fHu8cpWr4eGEA+/bzBPtjyoj5l4Yu+KXa8vpsfVz/w/e09Qlz5PTgsHb6RRgU94LqCvSDPbr57TU8+TpgwPld6jb074Qm/t9VcPgbXvL1DINe9UaWuPq/SvT1ubSG9UBxgPrw9kL6gplK/AHQIPuLnP762MPO+4GmqPiC4Cr/X+429Gt/XPYDzqr4xQ2M9tMyCPqt6WT72I3W+z6TtPSl5NT48MwE+WMl3vjY7Qr613Gm+Mv+Ivnug/T6i66K9Apyevvw0Lr4sSpm+sFbNPRuBOD5dwDu+lX33vaG9Wj55PQg+0sXGPnWTuD2bxiY+o61KPXpt1j0gl5g+J0rCPKYO8j1en6m+hH6ePntK/r7tu4K+uDxGvkWbo74WiAq/E4I1vl5NHjxgPCO+980dPuzCjz57wCy/AB6RPXpRuz0ZWGc+CjCsvEz7Jr73x4u+52/qPnv6qL0j2k6+awsvPnP2zrzXMc69ABp1PnDRiT1iu9u+pP46PR78xL0OiHA+y9clvRSvIr5A+JC9vfzOPKq1oL7+JrS90qysPddsJT48SuU+rkgcv5CeIj0MWji+ZJadvTmYDb3c9Ae+9diWPXno+75hMqW+zlUzPevGo77nxjQ9ou8uvfmeETwMdqO9YhCYvjnvf77ja88+uB0aPhPWdr7jNX8+lShbPspt+zz9o2+9XHKUvqD+Yz55yyW+vw8XvmeBjr7Scxu+8dRDPnL8qL4IILU9cCLaPVD7CT8MzTU+nZ7XPferLD8sgWQ++b+jvdf3wb2eRe89N4wCPPVJzj3FH3U+dvwXPRUAY73jUP89MqrMvRxFhj6ZnNK+oduLPmAhi75K0C8+y6CCvoUkMzwlyVO+JooQPm6mor3DRCO+74y2vUtaYT6GjbK7xEKVPjZXvT6gbiC9z4TePkbt/rxBKqU9hSX+PmH9D74eGEC+rixRPRKhsT0="

def load_data(datafile):
    uids = []
    fids = []
    features = []
    with open(datafile, "r", encoding="utf-8") as in_file:
        for i, line in enumerate(in_file):
            uid, feature = line.strip("\n").split(" ", 1)
            uids += [uid]
            fids += ["f" + str(i)]
            features += [feature]
    return uids, fids, features
    

def test_create(name, dim, url="http://localhost:8330/brpc_faiss_server/"):
    request_data = {
        "db_name": name,
        "feature_dim": dim,
        "feature_version": "v1",
        "search_type": 0,
        "similarity_type": "L2",
        "search_device": "cpu",
    }
    request_data = json.dumps(request_data)
    print(url + "create")
    result = requests.post(url=url + "create", data=request_data)
    
    return result


def test_search(query, db_name, url):
    feature = query.split(" ")[1]
    request_data = {
        "db_name": db_name,
        "b64_feature": feature,
        "topk": 10,
    }
    request_data = json.dumps(request_data)
    result = requests.post(url=url + "search", data=request_data)
    return result
    # names = map(
    #     lambda x: (x["cfid"].split("_")[0], x["distance"]),
    #     json.loads(result.text)["output"]["recall"]
    # )
    
    # for name in names:
    #     print(name)
    

url="http://localhost:8330/brpc_faiss_server/"

request_data = {
        "db_name": "word.test",
        "feature_dim": 200,
        "feature_version": "v1",
        "search_type": 0,
        "similarity_type": "L2",
        "search_device": "cpu",
}
request_data = json.dumps(request_data)

## create db
result = requests.post(url=url + "create", data=request_data)
print("result status:%s response:%s" % (result.status_code, result.text))


ann_dataset = BigannData1M("./bigann", n_split=3)
cids, fids, features = ann_dataset.get_chunk(0)
print("number of cids:%d" % len(cids))
print("number of fids:%d" % len(fids))

data = []
i = 0
for cid, fid, feature in list(zip(cids, fids, features)):
    item = {"cid": cid, "feature_id": fid, "b64_feature": feature}
    i = i + 1
    if i > 100:
        break
    data.append(item)

request_data = {
    "db_name": "word.test",
    "feature_version": "v1",
    "feature_dim": 200,
    "data": data,
}
request_data = json.dumps(request_data)
result = requests.post(url=url + "batch_add", data=request_data)
print("result status:%s response:%s" % (result.status_code, result.text))


result1 = test_search(QUERY1, "word.test", url)
print("result status:%s response:%s" % (result1.status_code, result1.text))

query = "hello " + data[0]["b64_feature"]

result1 = test_search(query, "word.test", url)
print("result status:%s response:%s" % (result1.status_code, result1.text))