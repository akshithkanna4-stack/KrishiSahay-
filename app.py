# app.py
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv
# ------------------ Load Hugging Face API Key ------------------
load_dotenv()  # loads .env file
HF_API_KEY = os.getenv("HF_API_KEY")

# Use a guaranteed free-tier model on HF Router
HF_MODEL_ID = "Qwen/Qwen2.5-72B-Instruct"
HF_API_URL = "https://router.huggingface.co/v1/chat/completions"

# ------------------ Flask App ------------------
app = Flask(__name__)
CORS(app) # Enable CORS for all routes

# ------------------ Weather API Function ------------------
def get_weather_data(lat=None, lon=None, city=None):
    """
    Fetch weather from Open-Meteo or wttr.in as a fallback.
    """
    try:
        if lat and lon:
            # Using Open-Meteo for coordinates
            url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            temp = data['current_weather']['temperature']
            code = data['current_weather']['weathercode']
            
            # Simple mapping for WMO weather codes
            # 0: Clear, 1-3: Cloudy, 45-48: Fog, 51-67: Rain/Drizzle, 71-77: Snow, 95-99: Thunderstorm
            desc = "Clear"
            if code in [1, 2, 3]: desc = "Cloudy"
            elif code in [45, 48]: desc = "Fog"
            elif 51 <= code <= 67: desc = "Rainy"
            elif 71 <= code <= 77: desc = "Snowy"
            elif code >= 95: desc = "Thunderstorms"
            
            # We don't have city name natively from open-meteo without another geocoding call, 
            # so we just say "Your Location"
            location_name = "Your Location"
            
            # Attempt to get city name via reverse geocoding if possible (OpenStreetMap Nominatim)
            try:
                geo_url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}"
                geo_resp = requests.get(geo_url, headers={'User-Agent': 'KrishiSahayApp/1.0'}, timeout=2)
                if geo_resp.ok:
                    geo_data = geo_resp.json()
                    location_name = geo_data.get('address', {}).get('city') or geo_data.get('address', {}).get('town') or geo_data.get('address', {}).get('village') or "Your Location"
            except:
                pass
                
            return {"temperature": temp, "description": desc, "location": location_name}
            
        elif city:
            # Using Nominatim to get lat/lon for city search
            geo_url = f"https://nominatim.openstreetmap.org/search?q={city}&format=json&limit=1"
            geo_resp = requests.get(geo_url, headers={'User-Agent': 'KrishiSahayApp/1.0'}, timeout=5)
            if geo_resp.ok and geo_resp.json():
                geo_data = geo_resp.json()[0]
                return get_weather_data(lat=geo_data['lat'], lon=geo_data['lon'])
            
            return None
    except Exception as e:
        print(f"Weather Fetch Error: {e}")
        return None

# ------------------ Hugging Face AI Function ------------------
def get_ai_response_hf(query, weather, location, lang="en"):
    """
    Send a prompt to Hugging Face API and return AI-generated farming advice.
    """
    if not HF_API_KEY:
        return "Server Error: Hugging Face API Key is missing. Please check the backend configuration."

    lang_instruction = ""
    if lang == "hi":
        lang_instruction = " Please provide your answer entirely in Hindi."
    elif lang == "te":
        lang_instruction = " Please provide your answer entirely in Telugu."

    system_prompt = (
        f"You are KrishiSahay, a helpful and expert AI agricultural assistant designed for farmers. "
        f"The farmer is located in {location} where the current weather is {weather}. "
        f"Provide practical, actionable advice in bullet points.{lang_instruction}"
    )

    try:
        headers = {
            "Authorization": f"Bearer {HF_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": HF_MODEL_ID,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query}
            ],
            "max_tokens": 400,
            "temperature": 0.5
        }
        
        response = requests.post(HF_API_URL, headers=headers, json=payload, timeout=60)
        response.raise_for_status() # Raise exception for bad status codes
        
        response_data = response.json()
        return response_data["choices"][0]["message"]["content"].strip()
    except Exception as e:
        import traceback
        err = traceback.format_exc()
        print(f"HuggingFace API Error: {err}", flush=True)
        return f"I apologize, but I am currently unable to generate advice. Error Details: {str(e)} | Trace: {err}"

# ------------------ Flask Routes ------------------
@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/api/weather", methods=["GET"])
def weather_api():
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    city = request.args.get('city')
    
    weather_data = get_weather_data(lat=lat, lon=lon, city=city)
    if weather_data:
        return jsonify(weather_data)
    else:
        return jsonify({"error": "Failed to fetch weather"}), 400

@app.route("/api/chat", methods=["POST"])
def chat_api():
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400
        
    query = data.get("query", "").strip()
    weather = data.get("weather", "Unknown weather").strip()
    location = data.get("location", "Unknown location").strip()
    lang = data.get("language", "en").strip()

    if not query:
        return jsonify({"error": "Empty query"}), 400

    # Get AI-generated response
    result_text = get_ai_response_hf(query, weather, location, lang)

    return jsonify({"response": result_text})

# ------------------ Run App ------------------
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)