import requests
from bs4 import BeautifulSoup
import csv
import re


def modifyString(string):
    finalString = ""
    listOfWords = string.split()
    for i in range(0, listOfWords.__len__()):
        word = re.sub(r"[^a-zA-Z0-9]+", '', listOfWords[i])
        if i == listOfWords.__len__() - 1:
            finalString += word
        else:
            if word != "":
                finalString += word + "-"

    return finalString.strip()


class Scraper:
    def __init__(self):
        global globalCounter
        globalCounter = 0

    def sendRequest(self, url):
        res = requests.get(url, headers={'user-agent': 'my-app/0.0.1'})
        soup = BeautifulSoup(res.text, 'lxml')
        return soup

    def getPaginationNumber(self, soup):
        result = soup.find_all('div', {"class": "col-l-4 mtop pagination-number"})
        return result[0].getText().split("of")[1].strip()

    def prepareString(self, soup, cityName):
        result = soup.find_all('a', {"class": "result-title hover_feedback zred bold ln24 fontsize0 "}, href=True)
        global globalCounter
        for item in range(0, result.__len__()):
            if result[item]['href'] is not None:
                globalCounter += 1
                print(result[item]['href'])
                self.requestRestaurantDetails(result[item]['href'], cityName)
                # self.writeCsv(globalCounter, result[item]['href'])
            else:
                print("Not Available")

                # for restaurantIndex in range(0, result.__len__()):
                #     finalName = modifyString(result[restaurantIndex].getText())
                #     finalAddress = modifyString(addressOne[restaurantIndex].getText())
                #     if finalName[finalName.__len__() - 1] == "-":
                #         print(finalName + finalAddress)
                #     else:
                #         print(finalName + "-" + finalAddress)

    def requestRestaurantDetails(self, url, cityName):
        restaurantUrl = url
        city = cityName
        res = requests.get(url, headers={'user-agent': 'my-app/0.0.1'})
        soup = BeautifulSoup(res.text, 'lxml')
        cuisinesObj = soup.find_all('div', {"class": "res-info-cuisines clearfix"})
        restaurantObj = soup.find_all('a', {"class": "ui large header left"})
        ratingsObj = soup.find_all('div', {"class": "rating_hover_popup res-rating pos-relative clearfix mb5"})
        phoneNumberObj = soup.find_all('span', {"class": "tel left res-tel"})
        addressObj = soup.find_all('div', {"class": "borderless res-main-address"})
        avgCostForTwoObj = soup.find_all('div', {"class": "res-info-detail"})
        isOpenNowObj = soup.find_all('span', {"class": "fontsize5 zgreen"})
        timingsObj = soup.find_all('div', {"class": "res-info-timings"})
        gpsLocationObj = soup.find_all('div', {"class": "resmap-img"})

        if cuisinesObj.__len__() > 0:
            cuisines = cuisinesObj[0].getText()
        else:
            cuisines = "Not Available"
        if restaurantObj.__len__() > 0:
            restaurantName = restaurantObj[0].getText()
        else:
            restaurantName = "Not Available"
        if phoneNumberObj.__len__() > 0:
            phoneNumber = phoneNumberObj[0].getText()
        else:
            phoneNumber = "Not Available"
        if addressObj.__len__() > 0:
            address = addressObj[0].getText()
        else:
            address = "Not Available"
        if avgCostForTwoObj.__len__() > 0:
            avgCostForTwoObj = avgCostForTwoObj[0].find_all('span', {"tabindex": "0"})
            if avgCostForTwoObj.__len__() > 0:
                avgCostForTwo = avgCostForTwoObj[0].getText()
            else:
                avgCostForTwo = "Not Available"
        else:
            avgCostForTwo = "Not Available"
        if isOpenNowObj.__len__() > 0:
            isOpenNow = isOpenNowObj[0].getText()
        else:
            isOpenNow = "Not Available"
        if timingsObj.__len__() > 0:
            timings = timingsObj[0].getText()
        else:
            timings = "Not Available"
        if ratingsObj.__len__() > 0:
            ratings = re.sub(r"[\n\t\s]*", "", ratingsObj[0].getText().strip())
        else:
            ratings = "Not Available"
        if gpsLocationObj.__len__() > 0:
            gpsLocation = gpsLocationObj[0]['data-url']
            startIndex = gpsLocation.index("center=") + 7
            endIndex = startIndex + 27
            gpsLocation = gpsLocation[startIndex : endIndex]
        else:
            gpsLocation = "Not Available"

        self.writeCsv(globalCounter, restaurantUrl, restaurantName, cuisines, ratings, address, gpsLocation,
                      avgCostForTwo, isOpenNow, timings, phoneNumber, city)

    def writeCsv(self, id, restaurantUrl, restaurantName, cuisines, ratings, address, gpsLocation,
                      avgCostForTwo, isOpenNow, timings, phoneNumber, city):
        with open('ZomatoRestaurantData.csv', 'a') as zomatoData:
            csvWriter = csv.writer(zomatoData, delimiter=',', quoting=csv.QUOTE_ALL)
            csvWriter.writerow([id, restaurantUrl.strip(), restaurantName.strip(),
                                cuisines.strip(), ratings.strip(), address.strip(), gpsLocation.strip(),
                                avgCostForTwo.strip(), isOpenNow.strip(), timings.strip(),
                                phoneNumber.strip(), city.strip()])


globalCounter = 0
columnData = ['id', 'RestaurantUrl', "RestaurantName", "Cuisines", "Ratings", "Address", "GpsLocation",
              "AvgCostOfTwo", "IsOpenNow", "PhoneNumber", "City"]
with open('ZomatoRestaurantData.csv', 'w') as zomatoData:
    csvWriter = csv.writer(zomatoData, delimiter=',', quoting=csv.QUOTE_ALL)
    csvWriter.writerow(columnData)

scraper = Scraper()
cityName = input("Please Enter City Name: ")
soup = scraper.sendRequest("https://www.zomato.com/" + cityName + "/Takeaway?page=1")
maxPageSize = scraper.getPaginationNumber(soup)
for i in range(0, int(maxPageSize)):
    soup = scraper.sendRequest("https://www.zomato.com/" + cityName + "/Takeaway?page=" + str(i))
    scraper.prepareString(soup, cityName)
