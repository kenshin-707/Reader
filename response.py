import requests

# Ask user for the website URL
url = input("Enter the website URL (e.g., https://example.com): ")

try:
    # Send a GET request
    response = requests.get(url)

    # Check if request was successful
    if response.status_code == 200:
        print("✅ Request successful!\n")
        print("Website Content Preview (first 500 chars):\n")
        print(response.text[:500])  # show only first 500 chars
        with open("output.txt", "w", encoding="utf-8") as f:
            f.write(response.text)
    else:
        print(f"❌ Failed to fetch the page. Status code: {response.status_code}")

except requests.exceptions.RequestException as e:
    print(f"⚠ Error: {e}")