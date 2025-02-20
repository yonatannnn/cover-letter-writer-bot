from flask import Flask, request, jsonify, send_from_directory
from database import users_collection
from ai_service import generate_cover_letter
import os
from dotenv import load_dotenv

load_dotenv()
PORT = int(os.getenv("PORT", 5000))

app = Flask(__name__)

@app.route('/set_experience', methods=['POST'])
def set_experience():
    data = request.json
    user_id = data.get('user_id')
    experience = data.get('experience')

    if not user_id or not experience:
        return jsonify({"error": "Missing user_id or experience"}), 400

    users_collection.update_one(
        {"user_id": user_id}, 
        {"$set": {"experience": experience}}, 
        upsert=True
    )
    return jsonify({"message": "Experience updated successfully"})

@app.route('/get_experience/<int:user_id>', methods=['GET'])
def get_experience(user_id):
    if not user_id:
        return jsonify({"error": "Missing user_id"}), 400

    user_data = users_collection.find_one({"user_id": user_id})
    if not user_data:
        return jsonify({"error": "User not found"}), 404

    return jsonify({"experience": user_data.get("experience")})

@app.route('/set_github', methods=['POST'])
def set_github():
    data = request.json
    user_id = data.get('user_id')
    github = data.get('github')

    if not user_id or not github:
        return jsonify({"error": "Missing user_id or github"}), 400

    users_collection.update_one(
        {"user_id": user_id}, 
        {"$set": {"github": github}}, 
        upsert=True
    )
    return jsonify({"message": "GitHub link updated successfully"})

@app.route('/set_portfolio', methods=['POST'])
def set_portfolio():
    data = request.json
    user_id = data.get('user_id')
    portfolio = data.get('portfolio')

    if not user_id or not portfolio:
        return jsonify({"error": "Missing user_id or portfolio"}), 400

    users_collection.update_one(
        {"user_id": user_id}, 
        {"$set": {"portfolio": portfolio}}, 
        upsert=True
    )
    return jsonify({"message": "Portfolio updated successfully"})

@app.route('/edit_experience', methods=['POST'])
def edit_experience():
    data = request.json
    user_id = data.get('user_id')
    new_experience = data.get('new_experience')

    if not user_id or not new_experience:
        return jsonify({"error": "Missing user_id or new_experience"}), 400

    users_collection.update_one(
        {"user_id": user_id}, 
        {"$set": {"experience": new_experience}}
    )
    return jsonify({"message": "Experience edited successfully"})

@app.route('/set_preferences', methods=['POST'])
def set_preferences():
    data = request.json
    user_id = data.get('user_id')
    preferences = data.get('preferences')

    if not user_id or not preferences:
        return jsonify({"error": "Missing user_id or preferences"}), 400

    users_collection.update_one(
        {"user_id": user_id}, 
        {"$set": {"preferences": preferences}}, 
        upsert=True
    )
    return jsonify({"message": "Preferences updated successfully"})

@app.route('/edit_preferences', methods=['POST'])
def edit_preferences():
    data = request.json
    user_id = data.get('user_id')
    new_preferences = data.get('new_preferences')

    if not user_id or not new_preferences:
        return jsonify({"error": "Missing user_id or new_preferences"}), 400

    users_collection.update_one(
        {"user_id": user_id}, 
        {"$set": {"preferences": new_preferences}}
    )
    return jsonify({"message": "Preferences edited successfully"})

@app.route('/set_profile', methods=['POST'])
def set_profile():
    data = request.json
    user_id = data.get('user_id')
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    experience = data.get('experience')
    preferences = data.get('preferences')
    github = data.get('github')
    portfolio = data.get('portfolio')
    additional_info = data.get('additional_info')

    if not user_id or not experience:
        return jsonify({"error": "Missing required fields"}), 400

    users_collection.update_one(
        {"user_id": user_id},
        {"$set": {
            "first_name":first_name,
            "last_name" : last_name,
            "experience": experience,
            "preferences": preferences,
            "github": github,
            "portfolio": portfolio,
            "additional_info" : additional_info
        }},
        upsert=True
    )
    return jsonify({"message": "Profile updated successfully"})

@app.route('/profile_form')
def profile_form():
    return send_from_directory('static', 'index.html')

@app.route('/get_profile/<int:user_id>', methods=['GET'])
def get_profile(user_id):
    if not user_id:
        return jsonify({"error": "Missing user_id"}), 400

    user_data = users_collection.find_one({"user_id": str(user_id)})
    if not user_data:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "first_name" : user_data.get("first_name" , ""),
        "last_name" : user_data.get("last_name" , ""),
        "experience": user_data.get("experience", ""),
        "preferences": user_data.get("preferences", ""),
        "github": user_data.get("github", ""),
        "portfolio": user_data.get("portfolio", ""),
        "additional_info" : user_data.get("additional_info", "")
    })

@app.route('/generate_cover_letter', methods=['POST'])
def generate_letter():
    data = request.json
    user_id = data.get('user_id')
    job_description = data.get('job_description')
    if not user_id or not job_description:
        return jsonify({"error": "Missing user_id or job_description"}), 400

    user_data = users_collection.find_one({"user_id": str(user_id)})
    if not user_data:
        return jsonify({"error": "User not found"}), 404
    print(user_data)
    cover_letter = generate_cover_letter(user_data, job_description)
    return jsonify({"cover_letter": cover_letter})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=PORT, debug=True)