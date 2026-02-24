import urllib.request
import threading
import time
from app import app, socketio

# Run the socketio app in a background thread for fetching routes locally
def run_app():
    socketio.run(app, debug=False, use_reloader=False, host='127.0.0.1', port=5003)

t = threading.Thread(target=run_app)
t.daemon = True
t.start()

time.sleep(3) # allow start

routes_to_test = ['/tab-1', '/tab-2', '/tab-3', '/tab-4']

print("--- TESTING ROUTES ---")
success = True
for r in routes_to_test:
    try:
        response = urllib.request.urlopen(f'http://127.0.0.1:5003{r}')
        if response.getcode() == 200:
            print(f"✅ Route {r} OK")
        else:
            print(f"❌ Route {r} Failed with code {response.getcode()}")
            success = False
    except Exception as e:
        print(f"❌ Route {r} Error: {e}")
        success = False

# graceful failure check
if not success:
    print("TEST FAILED")
else:
    print("ALL TESTS PASSED")
