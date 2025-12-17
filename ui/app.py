# Main Flask application for SIEM Event Dashboard
# Create and configure the Flask application

from flask import Flask
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ui.routes.event_routes import event_bp


def create_app():
    app = Flask(__name__, 
                template_folder='views/templates',
                static_folder='static')
    
    # Configuration
    app.config['SECRET_KEY'] = 'siem-event-dashboard-secret-key'
    app.config['JSON_SORT_KEYS'] = False
    
    # Register blueprints
    app.register_blueprint(event_bp)
    return app


if __name__ == '__main__':
    app = create_app()
    
    # Port can be configured via environment variable
    port = int(os.environ.get('PORT', 5000))
    
    print("🛡️ SIEM Event Dashboard starting...")
    print(f"📊 Access the dashboard at: http://localhost:{port}")
    print("🟢 Set PORT environment variable to use a different port")
    print("   Example: PORT=8000 python3 app.py")
    print("Press CTRL+C to stop the server")
    app.run(debug=True, host='0.0.0.0', port=port)
