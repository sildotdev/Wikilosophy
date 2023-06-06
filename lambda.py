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
        # Convert to string
        p = p.prettify()
        
        # Used to find 'href="', i.e. a link
        last_six_chars = ''
        
        parens = 0
        for i,char in enumerate(p):
            last_six_chars = (last_six_chars + char)[-6:]
            if char == '(':
                parens += 1
            elif char == ')':
                parens -= 1
            elif parens == 0 and last_six_chars == 'href="':
                # Finds end quote for 'href="', i.e. end of link
                end_quote_idx = p.find('"', i+1)
                
                # p[i+1:end_quote_idx] is what's between the quotes in 'href="..."'
                href_link = p[i+1:end_quote_idx]

                # A valid link has a form of `/wiki/<something>`
                match = re.search(wiki_link_pattern, href_link)
                
                # Is valid link
                if match:
                    page_title = match.group(1)
                    # print(page_title)
                    return page_title
                # else, keep looking
                
    # Return empty string if not found
    return ''

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
        
        # Path of pages to Philosophy.
        pages = []

        while page and page != "Philosophy" and page not in pages:
            pages.append(page)
            
            # Scrape the Wikipedia page
            url = f'https://en.wikipedia.org/wiki/{page}'
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            elements = soup.select('div.mw-parser-output p')
            
            page = get_next_page(elements)
            
        # Reached Philosophy!
        if page == 'Philosophy':
            pages.append(page)
            return {
                'statusCode': 200,
                'body': json.dumps(pages)
            }
        # Did not reach Philosophy!
        else:
            return {
                'statusCode': 200,
                'body': json.dumps(f'{original_page} does not lead to Philosophy!')
            }
    except Exception as e:
        return {
            'statusCode': 400,
            'body': json.dumps(str(e))
        }
