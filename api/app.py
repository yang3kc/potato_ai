from flask import Flask
from api.routes.search import search_bp

app = Flask(__name__)
app.register_blueprint(search_bp)

if __name__ == "__main__":
    app.run(debug=True)
