import req as fetch_fun
import filter as parser 
try :
    in_url = input("Enter URL: ")
    content = fetch_fun.run(in_url)
    results = parser.parse_site("cybersecuritynews", content)
    print (results)
except Exception as e:
    print(f"Error: {e}")
