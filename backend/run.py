# backend/run.py

from app import create_app

app = create_app()

if __name__ == '__main__':
    # Start the server - like turning on the LEGO castle lights
    app.run(debug=True, port=5000)