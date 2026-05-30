import pandas as pd
from flask import Flask, jsonify, request
from catboost import CatBoostClassifier

app = Flask(__name__)

model = CatBoostClassifier()
model.load_model('catboost_model_sber.cbm')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        json_data = request.json
        df_input = pd.DataFrame([json_data])
        proba = model.predict_proba(df_input)[0, 1]
        prediction = 1 if proba >= 0.5 else 0
        return jsonify({
            'target_action': prediction,
            'probability': round(float(proba), 4)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=False)

