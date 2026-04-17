from flask import Flask, request, render_template
import requests
import json
import os  

app = Flask(__name__)

url = "https://mlproject-ukaca.canadacentral.inference.ml.azure.com/score"

api_key = os.getenv("API_KEY")

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

@app.route("/", methods=["GET", "POST"])
def home():
    result = None

    if request.method == "POST":
        data = {
            "data": [[
                float(request.form["age"]),
                float(request.form["bmi"]),
                int(request.form["children"]),
                1 if request.form["smoker"] == "yes" else 0
            ]]
        }

        response = requests.post(url, headers=headers, data=json.dumps(data))

        if response.status_code == 200:
            result = response.json()
        else:
            result = response.text

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
