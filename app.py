from flask import Flask, request, render_template
import requests
import json
import os   # ✅ ADD THIS

app = Flask(__name__)

url = "https://mlproject-ukaca.canadacentral.inference.ml.azure.com/score"

api_key = os.getenv("API_KEY")

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}
