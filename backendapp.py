from flask import send_from_directory
import os

@app.route('/')
def index():
    return send_from_directory(os.path.join(app.root_path, 'frontend'), 'index.html')

@app.route('/<path:path>')
def static_proxy(path):
    return send_from_directory(os.path.join(app.root_path, 'frontend'), path)
from flask import Flask, request, jsonify
from flask_cors import CORS
from scipy.optimize import linprog

app = Flask(__name__)
CORS(app)

# Yiyecek bilgileri (100g başına)
foods = [
    {"name": "Tavuk göğsü", "cal": 165, "pro": 31, "fat": 3.6, "carb": 0, "price": 12},
    {"name": "Pirinç", "cal": 130, "pro": 2.7, "fat": 0.3, "carb": 28, "price": 5},
    {"name": "Brokoli", "cal": 55, "pro": 3.7, "fat": 0.6, "carb": 11, "price": 6},
    {"name": "Süt", "cal": 60, "pro": 3.2, "fat": 3.3, "carb": 5, "price": 4},
]

@app.route('/optimize-diet', methods=['POST'])
def optimize_diet():
    data = request.json
    cal_min = data.get("calorie_min", 0)
    pro_min = data.get("protein_min", 0)
    fat_max = data.get("fat_max", float("inf"))
    carb_min = data.get("carb_min", 0)

    # Maliyet vektörü
    cost = [f["price"] for f in foods]

    # Besin matrisleri
    A = [
        [-f["cal"] for f in foods],  # Kalori >= min
        [-f["pro"] for f in foods],  # Protein >= min
        [f["fat"] for f in foods],   # Yağ <= max
        [-f["carb"] for f in foods], # Karbonhidrat >= min
    ]
    b = [-cal_min, -pro_min, fat_max, -carb_min]

    # Her yiyecek için 0–1000g arası sınır
    bounds = [(0, 1000)] * len(foods)

    result = linprog(c=cost, A_ub=A, b_ub=b, bounds=bounds, method="highs")

    if result.success:
        plan = {foods[i]["name"]: round(result.x[i], 2) for i in range(len(foods))}
        plan["toplam_maliyet"] = round(result.fun, 2)
        return jsonify(plan)
    else:
        return jsonify({"error": "Uygun bir çözüm bulunamadı."}), 400

if __name__ == '__main__':
    app.run(debug=True)
