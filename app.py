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

    # Check API key
    if not api_key:
        return "API_KEY not set in Azure App Service", 500

    if request.method == "POST":
        try:
            # ✅ Correct Azure ML payload (12 features)
            data = {
                "input_data": {
                    "columns": [
                        "age", "sex", "bmi", "children", "smoker",
                        "Claim_Amount", "past_consultations",
                        "num_of_steps", "Hospital_expenditure",
                        "Number_of_procedures", "Annual_Salary", "region"
                    ],
                    "data": [[
                        float(request.form["age"]),
                        request.form["sex"],
                        float(request.form["bmi"]),
                        int(request.form["children"]),
                        request.form["smoker"],
                        float(request.form["Claim_Amount"]),
                        int(request.form["past_consultations"]),
                        int(request.form["num_of_steps"]),
                        float(request.form["Hospital_expenditure"]),
                        int(request.form["Number_of_procedures"]),
                        float(request.form["Annual_Salary"]),
                        request.form["region"]
                    ]]
                }
            }

            # Send request
            response = requests.post(url, headers=headers, json=data)

            print("Status:", response.status_code)
            print("Response:", response.text)

            if response.status_code == 200:
                result = response.json()
            else:
                error = f"API Error {response.status_code}: {response.text}"

        except Exception as e:
            error = f"Exception: {str(e)}"

    return render_template("index.html", result=result, error=error)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
