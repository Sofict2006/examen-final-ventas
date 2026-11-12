import json
import urllib.request

with urllib.request.urlopen("http://localhost:8080/health", timeout=5) as response:
    health = json.load(response)
assert health["metadatabase"]["status"] == "healthy", health
assert health["scheduler"]["status"] == "healthy", health
