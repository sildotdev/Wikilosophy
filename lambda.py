import json

import re
import requests

from bs4 import BeautifulSoup

pattern = r"/wiki/(.*)"


            
    
def get_next_page(elements):
    # Elements is list of `p` elements
    
    for p in elements:
        # Stringify the element to detect it
        p = str(p.encode().decode())

        last_five_chars = ''
        page_title = ''
        building_url = False
        opend = False
        parens = 0
        for c in p:
            last_five_chars = (last_five_chars + c)[-6:]
            if building_url and not opend:
                if c == '"':
                    match = re.search(pattern, page_title)
                        # Extract the captured group (text after "/wiki/")
                    if match:
                        extracted_text = match.group(1)
                        page_title = extracted_text
                        print(page_title)
                        break
                else:
                    page_title += c
            elif c == '(':
                parens +=1
                opend = True
            elif c == ')' and opend:
                parens -= 1
                if parens== 0:
                    opend=False
                    page_title = ""
            if last_five_chars == 'href="' and not opend:
                building_url = True
        if page_title:
            return page_title

def lambda_handler(event, context):
    try:
        # Extract path parameters
        path_parameters = event['pathParameters']
    
        # Assuming 'page' is the name of your URL parameter
        page = original_page = path_parameters['page']
        
        pages = []

        while page and page != "Philosophy" and page not in pages:
            pages.append(page)
            
            url = f'https://en.wikipedia.org/wiki/{page}'
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            elements = soup.select('div.mw-parser-output p')
            
            page = get_next_page(elements)
        
        if page == 'Philosophy':
            pages.append(page)
            return {
                'statusCode': 200,
                'body': json.dumps(pages)
            }
        else:
            return {
                'statusCode': 200,
                'body': json.dumps(f'{original_page} does not lead to Philosophy!')
            }
    except:
        return {
            'statusCode': 400,
            'body': json.dumps('Something failed.')
        }
