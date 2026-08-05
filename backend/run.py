# backend/run.py

from app import create_app

app = create_app()

if __name__ == '__main__':
    # Start the server - like turning on the LEGO castle lights
    port = int(os.environ.get('PORT', 5000))  # Use the PORT environment variable if available, otherwise default to 5000
    app.run(host='0.0.0.0', port=port, debug=True)  # Set debug=True for development mode