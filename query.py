import requests, json

url = "http://localhost:8330/brpc_faiss_server/status"
request_data = {
	"db_name": "word.emb",
}
request_data = json.dumps(request_data)
result = requests.post(url=url, data=request_data)
print("results %s %s" % (result.status_code, result.text))
