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
        
        # p elements with content do not have classes.
        if element.has_attr('class'):
            continue
        
        new_el = remove_parenthetical_phrases(str(element))
        a_list = element.select('a')
        for a in a_list:
            if a.has_attr('href') and not a.has_attr('class') and a['href'][0] == '/':
                try:
                    return a['href'][6:]
                except:
                    continue

def lambda_handler(event, context):

    try:
        # TODO: get page from user
        page = original_page = 'Semantics'
        
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
