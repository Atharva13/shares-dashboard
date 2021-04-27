from rest_framework.decorators import api_view
from rest_framework.response import Response
import redislite
import json
import pyarrow as pa

def redis_connection():
	redis_instance = redis_instance = redislite.Redis('/tmp/redis.db')
	return redis_instance

pageReset = False
prevSearch = ''

@api_view(['GET'])
def get_shares(request,*args,**kwargs):
	global pageReset, prevSearch
	if prevSearch == request.GET.get("search"):
		pageReset = False
	pageNo = request.GET.get("pageNumber")
	limit = request.GET.get("limit")
	search = request.GET.get("search")
	start = int(pageNo)*int(limit)
	stop = int(pageNo)*int(limit) + int(limit)
	context = pa.default_serialization_context()
	r = redis_connection()
	if r.exists('share'):
		shares = context.deserialize(r.get('share'))
		updatedShares = []
		shares = json.loads(shares.to_json(orient='records'))
		for i in range(0,len(shares)):
			if search in shares[i]["name"]:
				updatedShares.append(shares[i])
		shares = updatedShares
		if pageReset == False and prevSearch != search:
			pageReset = True
			start = 0
			stop = int(limit)
		totalShares = len(shares)
		totalPages = totalShares/int(limit)
		if(updatedShares != []):
			shares = shares[start:stop]
		print('Results from Cache')
		prevSearch = search
		response = {
		'shares' : shares,
		'totalPages' : totalPages,
		'totalShares' : totalShares,
		'msg': 'List of Shares',
		'pageReset' : pageReset
		}
	return Response(response,status=200)