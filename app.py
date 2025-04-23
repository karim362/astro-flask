
from flask import Flask, request, jsonify
import swisseph as swe

app = Flask(__name__)

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    try:
        date = data['date']  # 'YYYY-MM-DD'
        time = data['time']  # 'HH:MM'
        lat = float(data['lat'])
        lon = float(data['lon'])

        year, month, day = map(int, date.split('-'))
        hour, minute = map(int, time.split(':'))
        ut_time = hour + minute / 60.0
        jd = swe.julday(year, month, day, ut_time)

        swe.set_ephe_path(".")
        swe.set_topo(lon, lat, 0)

        planets_ids = {
            'Sun': swe.SUN,
            'Moon': swe.MOON,
            'Mercury': swe.MERCURY,
            'Venus': swe.VENUS,
            'Mars': swe.MARS,
            'Jupiter': swe.JUPITER,
            'Saturn': swe.SATURN
        }

        results = {}
        for name, pid in planets_ids.items():
            pos = swe.calc_ut(jd, pid)[0][0]
            results[name] = round(pos, 2)

        # حساب الطالع (البيت الأول)
        asc = swe.houses(jd, lat, lon.encode() if isinstance(lon, str) else lon)[0][0]
        results["Ascendant"] = round(asc, 2)

        return jsonify({"status": "success", "planets": results})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
