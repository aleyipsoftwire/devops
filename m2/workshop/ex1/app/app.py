from flask import Flask, render_template, request, redirect, url_for
import requests
import os


app = Flask(__name__)

@app.route('/')
def index():
    url = 'https://api.nasa.gov/planetary/apod'

    headers = {"Accept": "application/json"}

    query = {
        'api_key': os.environ["API_KEY"],
    }

    response = requests.request(
        "GET",
        url,
        headers=headers,
        params=query
    )

    res = response.json()

    hdurl = res['hdurl']
    title = res['title']
    explanation = res['explanation']
    
    
    return render_template('index.html', landing_image=hdurl, landing_title = title,  landing_explanation = explanation)

@app.route('/mars')
def mars():
    url = 'https://api.nasa.gov/mars-photos/api/v1/rovers/opportunity/photos'

    headers = {"Accept": "application/json"}

    query = {
        'api_key': os.environ["API_KEY"],
        'sol': 1,
        'page': 1,
        'camera': 'PANCAM'
    }

    response = requests.request(
        "GET",
        url,
        headers=headers,
        params=query
    )

    res = response.json()

    img_srcs = [photo['img_src'] for photo in res['photos']]
    
    return render_template('mars.html', img_srcs=img_srcs)

@app.route('/weather')
def weather():
    url = 'https://api.nasa.gov/insight_weather/'

    headers = {"Accept": "application/json"}

    query = {
        'api_key': os.environ["API_KEY"],
        'feedtype':'json',
        'ver':'1.0'
        # 'sol': 1,
        # 'page': 1,
        # 'camera': 'PANCAM'
    }

    response = requests.request(
        "GET",
        url,
        headers=headers,
        params=query
    )

    print(response)
    res = response.json()
    print(res)
    
    return render_template('weather.html')
