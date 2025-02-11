from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Токен для доступа к amoCRM
AMOCRM_ACCESS_TOKEN = "your_access_token"
AMOCRM_URL = "https://your_subdomain.amocrm.ru/api/v4/leads"

@app.route('/vk-webhook', methods=['POST'])
def vk_webhook():
    data = request.json
    if 'client_info' in data:
        lead_data = {
            "name": f"Лид из VK: {data['client_info'].get('name', 'Без имени')}",
            "responsible_user_id": 123456,  # ID менеджера в amoCRM
            "custom_fields_values": [
                {"field_code": "PHONE", "values": [{"value": data['client_info'].get('phone', '')}]},
                {"field_code": "EMAIL", "values": [{"value": data['client_info'].get('email', '')}]}
            ]
        }

        headers = {"Authorization": f"Bearer {AMOCRM_ACCESS_TOKEN}", "Content-Type": "application/json"}
        response = requests.post(AMOCRM_URL, json=[lead_data], headers=headers)

        return jsonify(response.json()), response.status_code

    return jsonify({"error": "Invalid data"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

