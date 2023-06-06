from bs4 import BeautifulSoup
import json
import re
import requests

# regex pattern to get title of next wikipedia page
wiki_link_pattern = r"/wiki/(.*)"

def get_next_page(paragraphs):
    """
    Helper function for the lambda do parse the paragraphs of a wikipedia page
    to find the first link to another wikipedia page, not counting first links
    in parentheses.

    Parameters
    ----------
    elements: (list('bs4.element.Tag'))
        Expected to be paragraphs of a wikipedia page. 

    Returns
    ------
    page_title: (string)
        The first string 
    """

    for p in paragraphs:
        #convert to string
        p = p.prettify()

        page_title = ""
        next_page  = ""
        last_six_chars = ""
        parsing_link = False

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
                if parens == 0:
                    in_paren = False
                    page_title = ""

            if last_six_chars == 'href="' and not in_paren:
                parsing_link = True
        
        # If a page title has been found, return
        # Otherwise check next paragraph
        if next_page: return next_page

def lambda_handler(event, context):
    """
    This function extracts the path parameter from the event, and follows a 
    chain of Wikipedia links starting from the given page until it reaches the
    "Philosophy" page or encounters a loop. It returns a list of pages visited 
    in the chain, or a message indicating that the original page does not lead 
    to Philosophy.

    Parameters
    ----------
    event: (dict) 
        The event object containing information about the event triggering the Lambda function.
        
        pathParameters: (dict)
            A dictionary containing path parameters.
        page: (str): 
            The name of the URL parameter specifying the starting page.

    context (LambdaContext):
        The context object representing the runtime information of the Lambda function.

    Returns
    ------
    response (dict):
        Response to be turned into json to respond to server.

        statusCode: 200/400
            OK or Bad Request
        
        body: list(string)  or string
            List of pages that take the path or message indicating a loop when
            trying to find path or if an error took place.
    """

    try:
        # Extract path parameters
        path_parameters = event['pathParameters']
    
        # Assuming 'page' is the name of your URL parameter
        page = original_page = path_parameters['page']
        
        pages = [page]

        while page and page != "Philosophy" and page not in pages:
            pages.append(page)
            
            url = f'https://en.wikipedia.org/wiki/{page}'
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            paragraphs = soup.select('div.mw-parser-output p')
            
            page = get_next_page(paragraphs)
        
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
