import subprocess
import time
import requests
import sys

# Start ngrok in background
print("Starting ngrok...")
import os
ngrok_path = os.path.join(os.path.dirname(__file__), "ngrok.exe")
process = subprocess.Popen(
    [ngrok_path, "http", "5000"],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL
)

# Wait for ngrok to start
print("Waiting for ngrok to initialize...")
time.sleep(5)

# Get the public URL from ngrok API
try:
    response = requests.get("http://localhost:4040/api/tunnels")
    data = response.json()

    # Find the HTTPS tunnel
    for tunnel in data.get('tunnels', []):
        if tunnel.get('proto') == 'https':
            public_url = tunnel.get('public_url')
            print(f"\n{'='*60}")
            print(f"SUCCESS! Your app is now publicly accessible at:")
            print(f"\n{public_url}")
            print(f"\n{'='*60}")
            print("\nShare this link with anyone to give them access to your app!")
            print("Login credentials: admin / admin123")
            print("\nPress Ctrl+C to stop ngrok when done.")
            print(f"{'='*60}\n")
            break
    else:
        print("Could not find HTTPS tunnel")
        sys.exit(1)

    # Keep script running so ngrok stays active
    try:
        process.wait()
    except KeyboardInterrupt:
        print("\nStopping ngrok...")
        process.terminate()

except requests.exceptions.RequestException as e:
    print(f"Error connecting to ngrok API: {e}")
    print("Make sure ngrok started successfully")
    process.terminate()
    sys.exit(1)
