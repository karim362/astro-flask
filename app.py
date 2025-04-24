from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
from astronomia import sun, moon, mercury, venus, mars, jupiter, saturn, uranus, neptune
from astronomia.time import julian
from functools import lru_cache
import logging
logging.basicConfig(level=logging.DEBUG)

@app.route("/calculate", methods=["PT"])
def calculate_chart():
    app.logger.info("Received request: %s", request.json)
    # ... باقي الكود ...
app = Flask(__name__)
# استبدل إعدادات CORS بهذا:
CORS(app, resources={
    r"/calculate": {
        "origins": ["*"],
        "methods": ["POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# أضف هذا قبل route الرئيسي
@app.route('/calculate', methods=['OPTIONS'])
def handle_options():
    return jsonify({"status": "success"}), 200
    # التحقق منCORS وجود البيانات المطلوبة
    if not request.is_json:
        return jsonify({"status": "error", "message": "Request must be JSON"}), 400
    
    data = request.get_json()
    required_fields = ["date", "time", "lat", "lon"]
    if not all(field in data for field in required_fields):
        return jsonify({"status": "error", "message": "Missing required fields"}), 400

    try:
        # تحليل التاريخ والوقت
        date_str = data["date"]
        time_str = data["time"]
        dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
        
        # التحقق من نطاقات خطوط الطول والعرض
        lat = float(data["lat"])
        lon = float(data["lon"])
        if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
            return jsonify({"status": "error", "message": "Invalid latitude or longitude"}), 400

        jd = julian.toJD(dt)
        result = calculate_positions(jd)

        return jsonify({
            "status": "success",
            "planets": result,
            "metadata": {
                "date": date_str,
                "time": time_str,
                "coordinates": {"lat": lat, "lon": lon}
            }
        })

    except ValueError as e:
        return jsonify({"status": "error", "message": "Invalid date/time format"}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@lru_cache(maxsize=128)
def calculate_positions(jd):
    """دالة مع تخزين مؤقت للحسابات المتكررة لنفس الوقت"""
    return {
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

if __name__ == "__main__":
    app.run(debug=True)
