from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
from astronomia import sun, moon, mercury, venus, mars, jupiter, saturn, uranus, neptune
from astronomia.time import julian

app = Flask(__name__)
CORS(app)

@app.route("/calculate", methods=["POST"])
def calculate_chart():
    try:
        data = request.get_json()
        date_str = data.get("date")
        time_str = data.get("time")
        lat = float(data.get("lat"))
        lon = float(data.get("lon"))

        dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
        jd = julian.toJD(dt)

        result = {
            "status": "success",
            "planets": {
                "الشمس": round(sun.position(jd).lon, 2),
                "القمر": round(moon.position(jd).lon, 2),
                "عطارد": round(mercury.position(jd).lon, 2),
                "الزهرة": round(venus.position(jd).lon, 2),
                "المريخ": round(mars.position(jd).lon, 2),
                "المشتري": round(jupiter.position(jd).lon, 2),
                "زحل": round(saturn.position(jd).lon, 2),
                "أورانوس": round(uranus.position(jd).lon, 2),
                "نبتون": round(neptune.position(jd).lon, 2),
            }
        }

        return jsonify(result)

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)
