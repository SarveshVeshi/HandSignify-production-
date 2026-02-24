import urllib.request
import urllib.error

try:
    response = urllib.request.urlopen('http://127.0.0.1:5005/video_feed')
    print("Success")
except urllib.error.HTTPError as e:
    print(f"HTTPError: {e.code}")
    print(e.read().decode('utf-8'))
except Exception as e:
    print(f"Other error: {e}")
