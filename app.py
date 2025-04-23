from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
from astronomia import planetposition, sun, moon, mercury, venus, mars, jupiter, saturn, uranus, neptune
from astronomia.time import julian

app = Flask(__name__)
CORS(app)  # تفعيل CORS

@app.route("/calculate", methods=["POST"])
def calculate_chart():
    try:
        data = request.get_json()
        date_str = data.get("date")
        time_str = data.get("time")
        lat = float(data.get("lat"))
        lon = float(data.get("lon"))

        dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
        jd = julian.Date(dt.year, dt.month, dt.day, dt.hour + dt.minute / 60)

        # تحميل الكواكب
        sun_pos = sun.position(jd)
        moon_pos = moon.position(jd)
        mercury_pos = mercury.position(jd)
        venus_pos = venus.position(jd)
        mars_pos = mars.position(jd)
        jupiter_pos = jupiter.position(jd)
        saturn_pos = saturn.position(jd)
        uranus_pos = uranus.position(jd)
        neptune_pos = neptune.position(jd)

        result = {
            "status": "success",
            "planets": {
                "الشمس": round(sun_pos.lon, 2),
                "القمر": round(moon_pos.lon, 2),
                "عطارد": round(mercury_pos.lon, 2),
                "الزهرة": round(venus_pos.lon, 2),
                "المريخ": round(mars_pos.lon, 2),
                "المشتري": round(jupiter_pos.lon, 2),
                "زحل": round(saturn_pos.lon, 2),
                "أورانوس": round(uranus_pos.lon, 2),
                "نبتون": round(neptune_pos.lon, 2),
            }
        }

        return jsonify(result)

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)
