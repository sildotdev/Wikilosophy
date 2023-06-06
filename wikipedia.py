import requests
from bs4 import BeautifulSoup
import re 

wiki_link_pattern = r"/wiki/(.*)"

def get_next_page(paragraphs):
    """
    Helper function for the lambda do parse the paragraphs of a wikipedia page
    to find the first link to another wikipedia page, not counting first links
    in parentheses.

    Parameters
    ----------
    elements: list('bs4.element.Tag')
        Expected to be paragraph objects with 

    Returns
    ------
    page_title: string
        The first string 

    """

    for p in paragraphs:
        #convert to string
        p = p.prettify()

        page_title = ""
        next_page  = ""
        last_six_chars = ""
        parsing_link = False

        # To ignore parentheses
        in_paren = False
        parens = 0

        for char in p:
            last_six_chars = (last_six_chars + char)[-6:]
            
            if parsing_link and not in_paren:
                if char == '"':
                    # Signifies end of link
                    match = re.search(wiki_link_pattern, page_title)
                    if match:
                        next_page = match.group(1)
                        print(next_page)
                        break
                else:
                    page_title += char

            elif char == '(':
                parens += 1
                in_paren = True

            elif char == ')' and in_paren:
                parens -= 1
                if parens== 0:
                    in_paren=False
                    page_title = ""

            if last_six_chars == 'href="' and not in_paren:
                parsing_link = True
        
        # If a page title has been found, return
        # Otherwise check next paragraph
        if next_page: return next_page
pages = []
page = original_page = "Penis"
while page and page != "Philosophy" and page not in pages:
    pages.append(page)
    
    url = f'https://en.wikipedia.org/wiki/{page}'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    paragraphs = soup.select('div.mw-parser-output p')
    
    page = get_next_page(paragraphs)

if page == 'Philosophy':
    pages.append(page)

# URL = "https://en.wikipedia.org/wiki/Telecommunications"
# pattern = r"/wiki/(.*)"

# page = "Quadrupedalism"
# print(page)
# while page != "Philosophy":
#     URL = "https://en.wikipedia.org/wiki/" + page
#     response = requests.get(URL)

#     # Create a BeautifulSoup object from the response content
#     soup = BeautifulSoup(response.content, 'html.parser')

#     # Find the first anchor tag (link) on the page

#     div = soup.find('div', id='mw-content-text').find('div', class_='mw-parser-output')
#     if div:
#         paragraphs = soup.find_all('p')
#         for p in paragraphs:
#             print(type(p))

#             p = p.prettify()
#             last_five_chars = ''
#             url = ''
#             building_url = False
#             opend = False
#             parens = 0
#             for c in p:
#                 last_five_chars = (last_five_chars + c)[-6:]
#                 if building_url and not opend:
#                     if c == '"':
#                         match = re.search(pattern, url)
#                          # Extract the captured group (text after "/wiki/")
#                         if match:
#                             extracted_text = match.group(1)
#                             page = extracted_text
#                             print(page)
#                             break
#                     else:
#                         url += c
#                 elif c == '(':
#                     parens +=1
#                     opend = True
#                 elif c == ')' and opend:
#                     parens -= 1
#                     if parens== 0:
#                         opend=False
#                         url = ""
#                 if last_five_chars == 'href="' and not opend:
#                     building_url = True
            
#             if url: break

            