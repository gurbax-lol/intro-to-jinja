from flask import Flask, render_template
from random import randint
from datetime import datetime
import requests

YOUR_NAME = "Gurbax"

app = Flask(__name__)
now = datetime.now()


def get_age(name):
    response = requests.get(url=f"https://api.agify.io/?name={name}")
    response.raise_for_status()
    data = response.json()
    return data["age"]


def get_gender(name):
    params = {
        "name": name
    }
    response = requests.get(url="https://api.genderize.io?", params=params)  # Alternatively, this is a more verbose
    # way of passing params. Use this for more complex URL params.
    response.raise_for_status()
    data = response.json()
    return data["gender"]


@app.route("/")
def home():
    random_number = randint(1, 35)
    return render_template("index.html",
                           num=random_number,  # The variables passed into the templates have
                           year=now.year,  # to be keyword arguments (**kwargs)
                           username=YOUR_NAME)


@app.route("/guess/<name>")  # for example www.example.com/guess/gurbax
def guess(name):
    return render_template("guess.html",
                           name=name.title(),  # > Gurbax
                           gender=get_gender(name),  # Male
                           age=get_age(name))  # > 61


@app.route("/blog/")
def get_blog():
    blog_url = "https://api.npoint.io/c790b4d5cab58020d391"
    response = requests.get(blog_url)
    response.raise_for_status()
    all_posts = response.json()
    return render_template("blog.html", posts=all_posts)


if __name__ == "__main__":
    app.run(debug=True)
