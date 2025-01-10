import requests
from bs4 import BeautifulSoup

# URL to scrape
url = "https://www.kolscan.io/leaderboard"

# Send a GET request
response = requests.get(url)

# Check if request was successful
if response.status_code == 200:
    # Parse the content using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Find all 'a' tags with href starting with '/account'
    account_links = [a['href'] for a in soup.find_all('a', href=True) if a['href'].startswith('/account')]
    
    # Print the extracted links
    # for link in account_links:
    #     print(link)
    print(len(account_links))
    with open("data/kols.txt", "w+") as f:
        for account in account_links:
            f.write(account.replace("/account/", ""))
            f.write("\n")
else:
    print(f"Failed to fetch the page. Status code: {response.status_code}")
