import os
import sys
import requests
from bs4 import BeautifulSoup
import json as JSON

def parse_moves(url='https://bulbapedia.bulbagarden.net/wiki/List_of_moves'):

    # Send an HTTP GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:

        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # List of moves
        moves = []

        # Get all of the rows in the table
        table_rows = soup.find_all('tr')

        # SKIP, Name, Type, Category, PP, Power, Accuracy, SKIP

        # Column headers which include a link
        HEADERS_WITH_LINK = ['name', 'type', 'category']

        # Column Headers
        HEADERS = ['number', 'name', 'type', 'category', 'pp', 'power', 'accuracy', 'gen']

        # Loop over the rows
        for row in table_rows:

            # Move Data Placeholder
            move = {}

            # Get the columns in the row
            row_cols = row.find_all('td')

            # If there are the same number of headers
            if len(row_cols) == len(HEADERS):

                # Loop over the number of columns
                for i in range(len(row_cols)):

                    # Get the col element
                    col = row_cols[i]

                    # Get the row header key
                    header = HEADERS[i]

                    # Placeholder
                    content = None

                    # If the header contains a linl
                    if header in HEADERS_WITH_LINK:
                        # Get the link from the column
                        link = col.find('a')

                        # Link is found
                        if link:
                            # Get the content from the link
                            content = str(link.get_text()).strip()
                        else:
                            print("No link")
                    else: 
                        # Get the text from the column
                        content = str(col.get_text()).strip()

                    # Not none
                    if content:
                        
                        # Accuracy column, and contains percentage
                        if header == 'accuracy' and '%' in content:

                            # Strip the percentage from the content
                            content = content.rstrip('%')

                        # If content is numeric
                        if content.isdigit():

                            # Parse number from content
                            content = int(content)

                        else: # Content is not numeric

                            # Convert content to lower case
                            content = content.lower()

                        # Set the header element to the content
                        move[header] = content

            # If all of the rows are found
            if len(move) == len(HEADERS):

                # Add move to moves
                moves.append(move)

    # Return moves list
    return moves

# If this is the main process
if __name__ == '__main__':

    # Get arguments
    args = sys.argv[1:]

    # Default output filename
    outfile = "out/moves.json"

    # If argument is provided
    if len(args) > 0:

        # Get the outfile from the args
        outfile = args[0]

    # Get the folder for the output file
    filedir = os.path.dirname(outfile)

    # Ensure the output directory exists
    os.makedirs(filedir, exist_ok=True)

    # Parse the moves from the remote site (default url)
    moves = parse_moves()

    # Dump the moves to a string, 2-space indentation
    moves_str = JSON.dumps(moves, indent=2)

    # Open the output file
    with open(outfile, "w+") as out:

        # Write the moves string to the file
        out.write(moves_str)