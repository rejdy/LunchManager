from flask import Flask, render_template
from bs4 import BeautifulSoup
import requests
import googlemaps

gmaps = googlemaps.Client(key='AIzaSyDWGoMIsK1Q3c2BWX9ULMvMCMG8aK4mNwI')

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', Restaurants = restaurants, Menus = menus, Iter = iteration)

restaurants = []
menus = []
iteration = []

def get_distance(name, distance):

    return False

def get_lunch_menu_sme(WebSite, iter):
    soup = BeautifulSoup(WebSite, 'lxml')

    tag = soup.find('div', class_='nazov-restauracie')
    title = tag.h1.text.replace('Košice', '')

    restaurants.append(title.strip())

    today_menu = soup.find('div', class_='dnesne_menu')

    menus.append([])
    try:
        for item in today_menu.find_all('div', class_='jedlo_polozka'):
            try:
                price = item.span.b.text
            except Exception as e:
                price = ' '

            for food in item.find_all('div', class_='left'):
                text = food.text.strip() + '    ' + price
                menus[iter].append(text)
    except Exception as e:
        print('No Menu')
        menus[iter].append(' ')


if __name__ == "__main__":
    with open("data.txt", "r") as ins:
           dataArray = []
           for line in ins:
               dataArray.append(line)

    iter = 0
    for item in dataArray:
        iteration.append(iter)
        source = requests.get(item).text
        if 'restauracie.sme.sk' in item:
            get_lunch_menu_sme(source, iter)
        iter += 1


    my_distance = gmaps.distance_matrix('Sturova 27 Kosice', 'Hlavna 4 Kosice', 'walking')
    print(my_distance['rows'][0]['elements'][0]['distance']['value'])

    app.run(debug=True)
