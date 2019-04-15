import requests
import csv

def getRestaurantDetails(id) :
	
	with open('restaurant.csv', 'a') as csvFile:
		url = "https://developers.zomato.com/api/v2.1/restaurant?res_id="+str(id)
		headers = { "user-key" : "8140a497cd4fc96c73c82b1eecc1da88"}
		r = requests.get(url, headers=headers)
		resjson = r.json()
		# print(resjson)
		rowlist = []
		rowlist.append(id)
		rowlist.append(resjson["name"])
		rowlist.append(resjson["location"]["address"])
		rowlist.append(resjson["location"]["locality"])
		rowlist.append(resjson["location"]["city"])
		rowlist.append(resjson["location"]["latitude"])
		rowlist.append(resjson["location"]["longitude"])
		rowlist.append(resjson["location"]["zipcode"])
		rowlist.append(resjson["cuisines"])
		rowlist.append(resjson["average_cost_for_two"])
		rowlist.append(resjson["user_rating"]["aggregate_rating"])
		rowlist.append(resjson["user_rating"]["rating_text"])

		# print(rowlist)
		writer = csv.writer(csvFile)
		writer.writerow(rowlist)		

def getReviewDetails(id) :
	with open('review.csv', 'a') as csvFile:
		url = "https://developers.zomato.com/api/v2.1/reviews?res_id="+str(id)
		headers = { "user-key" : "8140a497cd4fc96c73c82b1eecc1da88"}
		r = requests.get(url, headers=headers)
		resjson = r.json()
		# print(resjson)
		userreviewList = resjson["user_reviews"]
		for i in range(5) :
			review = userreviewList[i]["review"]
			# print(review)
			rowlist = []
			rowlist.append(id)
			rowlist.append(review["rating"])
			rowlist.append(review["review_text"])
			rowlist.append(review["rating_text"])
			rowlist.append(review["user"]["name"])
			rowlist.append(review["user"]["foodie_level"])
			rowlist.append(review["user"]["profile_url"])
			# print(rowlist)
			writer = csv.writer(csvFile)
			writer.writerow(rowlist)
		
  
for idone in range(1,30) : 
	url = "https://developers.zomato.com/api/v2.1/search?entity_id="+str(idone)+"&entity_type=city"
	headers = { "user-key" : "8140a497cd4fc96c73c82b1eecc1da88"}
	r = requests.get(url, headers=headers)

	print(r.status_code)
	resjson = r.json()
	print(type(resjson))

	offset = resjson["results_found"]
	print(offset)

	for step in range(0,81,20) :
		print("step :",step)
		headers = { "user-key" : "8140a497cd4fc96c73c82b1eecc1da88"}
		PARAMS = {'start':step} 
		data = {"positions":[0,6,7,29]}
		r = requests.get(url, params = PARAMS, headers=headers)

		# print(r.status_code)
		resjson = r.json()
		# print(type(resjson))
		listofRes = resjson["restaurants"]
		for i in range(20) :
			try :
				resid = listofRes[i]["restaurant"]["id"]
				print("restaurant ID : ",resid)
				getRestaurantDetails(resid)
				getReviewDetails(resid)
			except :
				print("Error in Parsing or getting data in Zomato")

