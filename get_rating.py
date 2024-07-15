import requests
from bs4 import BeautifulSoup

def get_title_text(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        span_tag = soup.find('span', attrs={'title': 'Difficulty'})
        if span_tag:
            difficulty_value = span_tag.get_text(strip=True)
            return difficulty_value[1 : ]
        else:
            return "ERROR1"    
    else:
        return "ERROR2"

url = input("Enter URL of problem : ")
if url[0] >= '0' and url[0] <= '9' :
    contest_id,problem_id = url.split() # 1328 C
    url = f"https://codeforces.com/contest/{contest_id}/problem/{problem_id}"
    title_text = get_title_text(url)
else: title_text = get_title_text(url)

print("problem rating :", title_text)

