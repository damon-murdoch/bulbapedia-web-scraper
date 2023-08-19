import os
import sys
import requests
from bs4 import BeautifulSoup
import json as JSON

def parse_pokemon(url='https://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_by_National_Pok%C3%A9dex_number'):

    # Send an HTTP GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:

        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # List of moves
        pokemon_list = []

        # Get all of the rows in the table
        table_rows = soup.find_all('tr')

        # SKIP, Name, Type, Category, PP, Power, Accuracy, SKIP

        # Column headers which include a link
        HEADERS_WITH_LINK = ['sprite', 'species', 'type', 'type2']

        # Column Headers
        HEADERS = ['dex', 'sprite', 'species', 'type1', 'type2']

        # Allowed Column Counts
        ALLOWED_COL_COUNT = [3,4,5]

        # If last dex number should be reused
        last_dex_number = None

        # Loop over the rows
        for row in table_rows:

            # Move Data Placeholder
            pokemon = {}

            # Get the columns in the row
            row_cols = row.find_all('td')

            # If there are the same number of headers
            # if len(row_cols) == len(HEADERS):

            # Skip next
            offset = 0

            # Placeholder
            col_expected = 0

            # Number of columns
            col_count = len(row_cols)

            # Row has valid column count
            if col_count in ALLOWED_COL_COUNT:
                # Set expected columns to counter - 1
                col_expected = col_count - 1
            else:
                # Divider
                if col_count == 0:
                    print("Region divider found, skipping ...")

                else: 
                    print(f"Unexpected column count: {col_count}, expected: {ALLOWED_COL_COUNT} ...")

                # Skip to next
                continue

            # Loop over the number of columns
            for i in range(col_count):

                # Get the col element
                col = row_cols[i]

                # Get the row header key
                header = HEADERS[i + offset]

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

                    # If this is the dex header, and is greater than 1
                    if header == 'dex':

                        # Get the rowspan property
                        rowspan = col.get('rowspan')

                        # Rowspan not null
                        if rowspan != None:

                            # Convert to int
                            rowspan_int = int(rowspan)

                            # Spans multiple rows
                            if rowspan_int > 1:
                                # Update last dex number
                                last_dex_number = content
                            else: # Only one row
                                # Clear last dex number
                                last_dex_number = None

                # Content is not defined
                if not content:

                    # Header is dex number and last dex number is not null
                    if header == 'dex' and last_dex_number != None:

                        # Set the dex number to the last dex
                        content = last_dex_number

                        # Increment expected columns
                        col_expected += 1

                        # Increment header offset
                        offset += 1

                # Not none
                if content:

                    # Species column
                    if header == 'species': 

                        # Find the small text        
                        small = col.find('small')

                        # If small is found
                        if small:

                            # Get the small text
                            form = small.get_text().lower()

                            # Text is not null
                            if form != "":

                                # Check for all of the different known formes
                                if form == "alolan form": content += '-alola'
                                elif form == "galarian form": content += '-galar'
                                elif form == "hisuian form": content += '-hisui'
                                elif form == "paldean form": content += '-paldea'
                                elif form == "sunny form": content += '-sunny'
                                elif form == "rainy form": content += '-rainy'
                                elif form == "snowy form": content += '-snowy'
                                elif form == "attack forme": content += '-attack'
                                elif form == "defense forme": content += '-defense'
                                elif form == "speed forme": content += '-speed'
                                elif form == "sunshine form": content += '-sunshine'
                                elif form == "east sea": content += '-east'
                                elif form == "sandy cloak": content += '-sandy'
                                elif form == "trash cloak": content += '-trash'
                                elif form == "heat rotom": content += '-heat'
                                elif form == "wash rotom": content += '-wash'
                                elif form == "frost rotom": content += '-frost'
                                elif form == "fan rotom": content += '-fan'
                                elif form == "mow rotom": content += '-mow'
                                elif form == "origin forme": content += '-origin'
                                elif form == "sky forme": content += '-sky'
                                elif form == "zen mode": content += '-zen'
                                elif form == "therian forme": content += '-therian'
                                elif form == "white kyurem": content += '-white'
                                elif form == "black kyurem": content += '-black'
                                elif form == "resolute form": content += '-resolute'
                                elif form == "pirouette forme": content += '-pirouette'
                                elif form == "genesect-douse drive": content += '-douse'
                                elif form == "genesect-shock drive": content += '-shock'
                                elif form == "genesect-burn drive": content += '-burn'
                                elif form == "genesect-chill drive": content += '-chill'
                                elif form == "blade forme": content += '-blade'
                                elif form == "neutral mode": content += '-neutral'
                                elif form == '50% forme': content += '-50%'
                                elif form == '10% forme': content += '-10%'
                                elif form == 'complete forme': content += '-complete'
                                elif form == 'hoopa unbound': content += '-unbound'
                                elif form == 'pom-pom style': content += '-pom-pom'
                                elif form == "pa’u style": content += "-pa'u"
                                elif form == "sensu style": content += "-sensu"
                                elif form == "sensu style": content += "-sensu"
                                elif form == "blue-striped form": content += "-blue-striped"
                                elif form == "white-striped form": content += "-white-striped"
                                elif form == "summer form": content += "-summer"
                                elif form == "autumn form": content += "-autumn"
                                elif form == "winter form": content += "-winter"
                                elif form == "red flower": content += "-red-flower"
                                elif form == "yellow flower": content += "-yellow-flower"
                                elif form == "orange flower": content += "-orange-flower"
                                elif form == "blue flower": content += "-blue-flower"
                                elif form == "white flower": content += "-white-flower"
                                elif form == "female": content += "-f"
                                elif form == "midnight form": content += "-midnight"
                                elif form == "dusk form": content += "-dusk"
                                elif form == "school form": content += "-school"
                                elif form == "meteor form": content += "-meteor"
                                elif form == "busted form": content += "-busted"
                                elif form == "dusk mane": content += "-dusk-mane"
                                elif form == "dawn wings": content += "-dawn-wings"
                                elif form == "gulping form": content += "-gulping"
                                elif form == "gorging form": content += "-gorging"
                                elif form == "low key form": content += "-low-key"
                                elif form == "noice face": content += "-noice"
                                elif form == "hangry mode": content += "-hangry"
                                elif form == "crowned sword": content += "-crowned"
                                elif form == "crowned shield": content += "-crowned"
                                elif form == "rapid strike style": content += "-rapid-strike"
                                elif form == "ice rider": content += "-ice-rider"
                                elif form == "shadow rider": content += "-shadow-rider"
                                elif form == "family of four": content += "-four"
                                elif form == "blue plumage": content += "-blue"
                                elif form == "yellow plumage": content += "-yellow"
                                elif form == "white plumage": content += "-white"
                                elif form == "hero form": content += "-hero"
                                elif form == "droopy form": content += "-droopy"
                                elif form == "stretchy form": content += "-stretchy"
                                elif form == "three-segment form": content += "-three-segment"
                                elif form == "roaming form": content += "-roaming"
                                elif form not in [
                                    'one form', 'normal', 'kyogre', 
                                    'groudon', 'normal forme', 'plant cloak',
                                    'overcast form', 'west sea', 'rotom', 
                                    'altered forme', 'land forme', 'arceus', 
                                    'red-striped form', 'standard mode', 'spring form', 
                                    'incarnate forme', 'kyurem', 'ordinary form', 
                                    'aria forme', 'genesect', 'meadow pattern', 
                                    'natural forme', 'male', 'shield forme', 
                                    'active mode', 'hoopa confined', 'baile style',
                                    'midday form', 'solo form', 'type: normal', 
                                    'red core', 'disguised form', 'amped form', 
                                    'vanilla cream', 'ice face', 'full belly mode', 
                                    'hero of many battles', 'single strike style', 
                                    'family of three', 'green plumage', 'zero form', 
                                    'curly form', 'two-segment form', 'chest form', 
                                    'apex build', 'ultimate mode', 'natural form'
                                ]: print(f"Unhandled forme: '{form}'")

                    # Accuracy column, and contains percentage
                    if header == 'dex' and '#' in content:

                        # Strip the percentage from the content
                        content = content.lstrip('#')

                    # If content is numeric
                    if content.isdigit():

                        # Parse number from content
                        content = int(content)

                    else: # Content is not numeric

                        # Convert content to lower case
                        content = content.lower()

                    # Set the header element to the content
                    pokemon[header] = content

            # If all of the rows are found
            if len(pokemon) == col_expected:

                # Add move to moves
                pokemon_list.append(pokemon)

            else: # Unexpected column count
                print(f"Unexpected columns found: {len(pokemon)}, expected: {col_expected}")

    # Return moves list
    return pokemon_list

# If this is the main process
if __name__ == '__main__':

    # Get arguments
    args = sys.argv[1:]

    # Default output filename
    outfile = "out/pokemon.json"

    # If argument is provided
    if len(args) > 0:

        # Get the outfile from the args
        outfile = args[0]

    # Get the folder for the output file
    filedir = os.path.dirname(outfile)

    # Ensure the output directory exists
    os.makedirs(filedir, exist_ok=True)

    # Parse the moves from the remote site (default url)
    pokemon = parse_pokemon()

    # Dump the moves to a string, 2-space indentation
    pokemon_str = JSON.dumps(pokemon, indent=2)

    # Open the output file
    with open(outfile, "w+") as out:

        # Write the moves string to the file
        out.write(pokemon_str)