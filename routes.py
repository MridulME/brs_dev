from flask import Blueprint, request, jsonify
from recommendation import recommend_by_user_id, recommend_by_interest_area
from database import *

recommend_bp = Blueprint('recommend', __name__)
book_df, user_df = get_data()
#book_df, user_df = det_data_ssh()

# Flask endpoint to recommend books based on user ID
@recommend_bp.route('/recommend', methods=['GET'])
def recommend():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    try:
        user_id = int(user_id)
        recommendations = recommend_by_user_id(user_df, user_id)
        if isinstance(recommendations, list):
            return jsonify(recommendations), 200
        else:
            return jsonify({"message": recommendations}), 200
    except ValueError:
        return jsonify({"error": "Invalid user ID"}), 400
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {e}"}), 500

# Flask endpoint to recommend books based on interest area
@recommend_bp.route('/recommend_by_interest', methods=['GET'])
def recommend_by_interest():
    interest_area = request.args.get('interest_area')
    if not interest_area:
        return jsonify({"error": "Interest area is required"}), 400

    try:
        recommendations = recommend_by_interest_area(interest_area)
        if isinstance(recommendations, list):
            return jsonify(recommendations), 200
        else:
            return jsonify({"message": recommendations}), 200
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {e}"}), 500
