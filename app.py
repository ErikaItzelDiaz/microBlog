import datetime
import os
from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from dotenv import load_dotenv
from bson import ObjectId

load_dotenv()
def create_app():
    app = Flask(__name__)
    client = MongoClient(os.getenv("MONGODB_URI"))
    app.db = client.microblog

    @app.route("/",methods=["GET","POST"])
    def home():
        if request.method == "POST":
            entry_content = request.form.get("content")
            formatted_date = datetime.datetime.today().strftime("%y-%m-%d")
            app.db.entries.insert_one({"content":entry_content,"date":formatted_date})
        entries_with_date = [
            (
                entry["_id"],
                entry["content"],
                entry["date"],
                datetime.datetime.strptime(entry["date"],"%y-%m-%d").strftime("%b %d")
            )
            for entry in app.db.entries.find({})
        ]
        latest_first = entries_with_date.copy()
        latest_first.reverse()
        return render_template("home.html",entries=latest_first)

    @app.route('/delete/<entry_id>', methods=['POST', 'DELETE'])
    def delete_entry(entry_id):
        if request.method in ['POST', 'DELETE']:
            entry_id_obj = ObjectId(entry_id)
            app.db.entries.delete_one({'_id': entry_id_obj})
        return redirect(url_for('home'))

    @app.route("/calendar/")
    def calendar():
        return render_template("comingSoon.html")
    @app.route("/about/")
    def about():
        return render_template("about.html")

    return app


app = create_app()

if __name__ == '__main__':
    app.run()