# backend/run.py
import os
from app import create_app

app = create_app()

if __name__ == '__main__':
    # Start the server - like turning on the LEGO castle lights
    # Use port 5001 in development to avoid conflicts with services that also use 5000.
    port = int(os.environ.get('PORT', 5001))  # Use the PORT environment variable if available, otherwise default to 5001
    app.run(host='0.0.0.0', port=port, debug=True)  # Set debug=True for development mode