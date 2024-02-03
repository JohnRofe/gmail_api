'''
Module to parse an HTML file and extract specific data. This was use because the email of interest was a html table "image"
'''

from bs4 import BeautifulSoup

def parse_html(html):
    '''
    Parses an HTML string and extracts specific data.

    Parameters:
    html (str): The HTML string to parse.

    Returns:
    list: The extracted data.
    '''
    soup = BeautifulSoup(html, 'html.parser')

    # Define the fields we're interested in, they can be changed depending on the content of the body
    fields = ['YOUR COLUMNS']

    # Find all 'p' tags and extract the text, stripping any whitespace
    cleaned_p_tags = [tag.get_text(strip=True) for tag in soup.find_all('p')]

    # Create a dictionary where the keys are the fields and the values are the corresponding values from the 'p' tags
    data = {field: cleaned_p_tags[i+1] for i, field in enumerate(cleaned_p_tags) if field in fields}

    # Convert the dictionary values to a list and return it
    return list(data.values())

def main():
    '''
    Main function to parse the HTML file and print the extracted data.
    '''
    with open('decoded.html', 'r') as file:
        html = file.read()

    print(parse_html(html))

if __name__ == '__main__':
    main()




