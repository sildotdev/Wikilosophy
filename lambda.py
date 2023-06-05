import json

import re
import requests

from bs4 import BeautifulSoup

def remove_parenthetical_phrases(string):
    output = ""
    stack = []
    for char in string:
        if char == '(':
            stack.append('(')
        elif char == ')':
            if stack:
                stack.pop()
            else:
                stack.append(')')
        elif not stack:
            output += char
    return BeautifulSoup(output, 'html.parser')
    
def get_next_page(elements):
    for element in elements:
        # Makes element withouth parentheses.
        new_el = remove_parenthetical_phrases(str(element))

        # Gets all `a` tagged elements.
        a_list = new_el.select('a')
        
        for a in a_list:
            # Get proper links, not references to parts of page.
            if a.has_attr('href') and a['href'][0] == '/':
                try:
                    # href is in format '/wiki/...'. This is getting the page directly.
                    return a['href'][6:]
                except:
                    continue

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
