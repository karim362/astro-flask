from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
from astronomia import sun, moon, mercury, venus, mars, jupiter, saturn, uranus, neptune
from astronomia.time import julian
import logging

app = Flask(__name__)

# إعدادات CORS شاملة
CORS(app, resources={
    r"/calculate": {
        "origins": "*",
        "methods": ["POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# إعداد التسجيل
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/calculate', methods=['OPTIONS'])
def handle_options():
    return jsonify({"status": "success"}), 200

@app.route("/calculate", methods=["POST"])
def calculate_chart():
    logger.info("Received request: %s", request.json)
    
    if not request.is_json:
        logger.error("Request is not JSON")
        return jsonify({"status": "error", "message": "Request must be JSON"}), 400
    
    data = request.get_json()
    required_fields = ["date", "time", "lat", "lon"]
    
    if not all(field in data for field in required_fields):
        logger.error("Missing fields: %s", data)
        return jsonify({"status": "error", "message": "Missing required fields"}), 400

    try:
        # معالجة الوقت بتنسيقات مختلفة
        time_str = data["time"].replace('ص', 'AM').replace('م', 'PM').split(' ')[0]
        
        if len(time_str.split(':')) == 2:  # إذا كان التنسيق HH:MM
            dt = datetime.strptime(f"{data['date']} {time_str}", "%Y-%m-%d %H:%M")
        else:  # إذا كان التنسيق HH:MM:SS
            dt = datetime.strptime(f"{data['date']} {time_str}", "%Y-%m-%d %H:%M:%S")
            
        jd = julian.toJD(dt)
        
        result = {
            "status": "success",
            "planets": {
                "الشمس": round(sun.position(jd).lon, 2),
                "القمر": round(moon.position(jd).lon, 2),
                # ... (باقي الكواكب)
            }
        }
        
        logger.info("Calculation successful: %s", result)
        return jsonify(result)

    except Exception as e:
        logger.exception("Calculation failed")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
