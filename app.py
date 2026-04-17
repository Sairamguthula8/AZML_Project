from flask import Flask, request, render_template
import requests
import json
import os

app = Flask(__name__)

# Get values from environment (best practice)
url = os.getenv("ML_URL", "https://mlproject-ukaca.canadacentral.inference.ml.azure.com/score")
api_key = os.getenv("API_KEY")

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    error = None

    # 🔍 Check API key early (prevents crash)
    if not api_key:
        return "❌ API_KEY not set in Azure App Service", 500

    if request.method == "POST":
        try:
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
                error = f"API Error: {response.status_code} - {response.text}"

        except Exception as e:
            error = f"Exception: {str(e)}"

    return render_template("index.html", result=result, error=error)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
