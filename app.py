from flask import Flask, jsonify, request, render_template
import requests

app = Flask(__name__, template_folder="templates", static_folder="static")

# Replace with your OpenWeatherMap API key
API_KEY = "your_openweathermap_api_key"
BASE_URL = "https://api.openweathermap.org/data/2.5"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/weather", methods=["GET"])
def get_weather():
    city = request.args.get("city", "Unknown")
    if not city:
        return jsonify({"error": "City not specified"}), 400

    params = {
        "q": city,
        "appid": 'f288d15c0521db4bcb9a813b85c2bbc0',
        "units": "metric",
    }
    response = requests.get(f"{BASE_URL}/weather", params=params)

    if response.status_code == 200:
        data = response.json()
        weather_data = {
            "city": data["name"],
            "temperature": f"{data['main']['temp']}°C",
            "condition": data["weather"][0]["description"].capitalize(),
        }
        return jsonify(weather_data)
    else:
        return jsonify({"error": "City not found"}), 404

@app.route("/forecast", methods=["GET"])
def get_forecast():
    city = request.args.get("city", "Unknown")
    if not city:
        return jsonify({"error": "City not specified"}), 400

    params = {
        "q": city,
        "appid": 'f288d15c0521db4bcb9a813b85c2bbc0',
        "units": "metric",
    }
    response = requests.get(f"{BASE_URL}/forecast", params=params)

    if response.status_code == 200:
        data = response.json()
        forecast = [
            {
                "datetime": item["dt_txt"],
                "temperature": f"{item['main']['temp']}°C",
                "condition": item["weather"][0]["description"].capitalize(),
            }
            for item in data["list"]
        ]
        return jsonify({"city": data["city"]["name"], "forecast": forecast})
    else:
        return jsonify({"error": "City not found"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
