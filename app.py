from flask import Flask
from src.middleware.routes import configure_routes
import os

app = Flask(__name__, template_folder='src/templates')

configure_routes(app)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)