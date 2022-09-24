import requests
import json

url = " http://localhost:8330/brpc_faiss_server/create"
request_data = {
	"db_name": "word.emb",
	"feature_dim": 200,
	"feature_version": "v1",
	"search_type": 0,
	"similarity_type": "L2",
	"search_device": "cpu",
}
request_data = json.dumps(request_data)
result = requests.post(url=url, data=request_data)
print("result status:%s response:%s" % (result.status_code, result.text))
