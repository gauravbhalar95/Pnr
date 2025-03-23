from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
import requests

# Flask App Setup
app = Flask(__name__)

# MongoDB Setup
MONGO_URI = "mongodb+srv://Forwardbot:Gaurav74@cluster0.vi2h4.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URI)
db = client.PNRTracker
pnr_collection = db.tracked_pnrs

# API Key
RAPIDAPI_KEY = "425e3f1022mshd7d4a2d9b3b0136p1fe9b1jsn0bd8321421c7"

# Function to fetch PNR status
def get_pnr_status(pnr_number):
    url = f"https://irctc1.p.rapidapi.com/api/v2/getPNRStatus?pnrNumber={pnr_number}"
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": "irctc1.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers)
    return response.json() if response.status_code == 200 else None

# Home Page - View Tracked PNRs
@app.route("/")
def index():
    tracked_pnrs = list(pnr_collection.find({}, {"_id": 0}))
    return render_template("index.html", pnrs=tracked_pnrs)

# Add PNR for Tracking
@app.route("/add", methods=["POST"])
def add_pnr():
    pnr_number = request.form.get("pnr_number")
    mobile = request.form.get("mobile")
    
    data = get_pnr_status(pnr_number)
    if data:
        status = data.get("passengerStatus", [{}])[0].get("currentStatus", "Unknown")
        pnr_collection.update_one({"pnr": pnr_number}, {"$set": {"mobile": mobile, "last_status": status}}, upsert=True)
    
    return redirect(url_for("index"))

# Delete PNR from Tracking
@app.route("/delete/<pnr>")
def delete_pnr(pnr):
    pnr_collection.delete_one({"pnr": pnr})
    return redirect(url_for("index"))

# Fetch Live PNR Status
@app.route("/status/<pnr>")
def status(pnr):
    data = get_pnr_status(pnr)
    return data if data else {"error": "PNR Not Found"}

if __name__ == "__main__":
    app.run(debug=True)
