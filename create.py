import requests
import json
import struct
import base64
import uuid

url = "http://localhost:8330/brpc_faiss_server/"
DIMENSION = 4

def create(db_name):
	request_data = {
		"db_name": db_name,
		"feature_dim": DIMENSION,
		"feature_version": "v1",
		"search_type": 0,
		"similarity_type": "L2",
		"search_device": "cpu",
	}
	request_data = json.dumps(request_data)
	result = requests.post(url=url + "create", data=request_data)
	print("create result status:%s response:%s" % (result.status_code, result.text))


def vect_feature(vector):
	dim = len(vector)
	bytearr = bytearray(4 * dim) ## each float need 4 bytes
	for i in range(dim):
		bytearr[i*4:i*4+4] = struct.pack('f', vector[i])
	vec = bytes(bytearr)
	
	float_vector = []
	for i in range(dim):
		float_vector.append(struct.unpack('f', vec[i*4:i*4+4])[0])
	#print("======== size of vector:%s" % len(float_vector) )
	#print("======== decoded vector:%s" % float_vector )

	feature = base64.b64encode(vec)
	print("feature:%s" % feature)
	feature = feature.decode("utf-8", "ignore")
	return feature

vect1 = [3.0, 4.0, 6.0, 7.1] 
vect2 = [9.0, 10.0, 11.0, 12.0]
vect3 = [10.5, 15.0, 12.0, 20.5]
vect4 = [20.0, 25.0, 23.0, 30.5]
vect5 = [22.0, 28.0, 26.0, 32.0]

def insert(db_name):
	#create("word.emb")
	#fid = str(uuid.uuid1())

	cids = [str(i) for i in range(5)]
	fids = [str(uuid.uuid1()) for i in range(5)]
	features = []
	features.append(vect_feature(vect1))
	features.append(vect_feature(vect2))
	features.append(vect_feature(vect3))
	features.append(vect_feature(vect4))
	features.append(vect_feature(vect5))

	data = []
	i = 0
	for cid, fid, feature in list(zip(cids, fids, features)):
		item = {"cid": cid, "feature_id": fid, "b64_feature": feature}
		data.append(item)

	request_data = {
		"db_name": db_name,
		"feature_version": "v1",
		"feature_dim": DIMENSION,
		"data": data,
	}
	request_data = json.dumps(request_data)
	result = requests.post(url=url + "batch_add", data=request_data)
	print("batch_add result status:%s response:%s" % (result.status_code, result.text))

def search(query_vector, db_name):
    feature = vect_feature(query_vector)
    request_data = {
        "db_name": db_name,
        "b64_feature": feature,
        "topk": 10,
    }
    request_data = json.dumps(request_data)
    result = requests.post(url=url + "search", data=request_data)
    print("search result status:%s response:%s" % (result.status_code, result.text))
    return result

create('db-of-dim-4')
insert('db-of-dim-4')

result = search(vect5, 'db-of-dim-4')
print("result:%s" % result)