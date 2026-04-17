from flask import Flask, request, render_template
import requests
import os

app = Flask(__name__)

# Environment variables
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

    if not api_key:
        return "API_KEY not set in Azure App Service", 500

    if request.method == "POST":
        try:
            # Correct input format for Azure ML
            data = {
                "input_data": {
                    "data": [[
                        float(request.form["age"]),
                        float(request.form["bmi"]),
                        int(request.form["children"]),
                        1 if request.form["smoker"] == "yes" else 0
                    ]]
                }
            }

            # Use json= (important)
            response = requests.post(url, headers=headers, json=data)

            # Debug print (will show in logs)
            print("Response Status:", response.status_code)
            print("Response Text:", response.text)

            if response.status_code == 200:
                res_json = response.json()

                # Extract prediction safely
                if isinstance(res_json, dict):
                    result = res_json
                else:
                    result = str(res_json)

            else:
                error = f"API Error {response.status_code}: {response.text}"

        except Exception as e:
            error = f"Exception: {str(e)}"

    return render_template("index.html", result=result, error=error)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
