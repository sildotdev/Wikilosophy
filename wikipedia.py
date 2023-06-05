import requests
from bs4 import BeautifulSoup
import re 



URL = "https://en.wikipedia.org/wiki/Telecommunications"
pattern = r"/wiki/(.*)"

page = "Albert_Einstein"
print(page)
while page != "Philosophy":
    URL = "https://en.wikipedia.org/wiki/" + page
    response = requests.get(URL)

    # Create a BeautifulSoup object from the response content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the first anchor tag (link) on the page

    div = soup.find('div', id='mw-content-text').find('div', class_='mw-parser-output')
    if div:
        paragraphs = soup.find_all('p')
        for p in paragraphs:
            p = str(p.encode().decode())
            last_five_chars = ''
            url = ''
            building_url = False
            opend = False
            parens = 0
            for c in p:
                last_five_chars = (last_five_chars + c)[-6:]
                if building_url and not opend:
                    if c == '"':
                        match = re.search(pattern, url)
                         # Extract the captured group (text after "/wiki/")
                        if match:
                            extracted_text = match.group(1)
                            page = extracted_text
                            print(page)
                            break
                    else:
                        url += c
                elif c == '(':
                    parens +=1
                    opend = True
                elif c == ')' and opend:
                    parens -= 1
                    if parens== 0:
                        opend=False
                        url = ""
                if last_five_chars == 'href="' and not opend:
                    building_url = True
            
            if url: break

            