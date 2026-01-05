import requests
import sys

try:
    print("Testing Production /students...")
    url = "https://fast-api-server-bi71.onrender.com/students"

    # 1. Check Content
    try:
        r = requests.get(url, timeout=10)
        print(f"GET Status: {r.status_code}")
        print(f"Body: {r.text}")
    except Exception as e:
        print(f"GET Failed: {e}")

    # 2. Check CORS for Vercel
    origin = "https://react-vite-deploy-umber-psi.vercel.app"
    try:
        r = requests.get(url, headers={"Origin": origin}, timeout=10)
        print(f"CORS Origin: {origin}")
        print(
            f"Access-Control-Allow-Origin: {r.headers.get('access-control-allow-origin')}"
        )
    except Exception as e:
        print(f"CORS Check Failed: {e}")

except Exception as e:
    print(f"Script Failed: {e}")
