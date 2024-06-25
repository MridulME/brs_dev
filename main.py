from flask import Flask
from routes import recommend_bp

app = Flask(__name__)
app.register_blueprint(recommend_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
