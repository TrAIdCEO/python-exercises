### Fetches a document's HTML and uses a parser to extract coordinate and character data, from a table within the document, into a dictionary.  
### Identifies the maximum boundaries of the grid and then iterates through the coordinates, printing each character at its specified position.
### Prints the y-coordinates in descending order since the output needs to be constructed top to bottom (and the x-coordinates ascending, as this is the natural left to right order).

### Example Usage:
### print_secret_message("https://docs.google.com/document/d/e/2PACX-1vTMOmshQe8YvaRXi6gEPKKlsC6UpFJSMAk4mQjLm_u1gmHdVVTaeh7nBNFBRlui0sTZ-snGwZM4DBCT/pub")

import urllib.request
from html.parser import HTMLParser

### Parser
class GoogleDocTableParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_table = False
        self.in_row = False
        self.in_cell = False
        self.current_cell_data = ""
        self.rows = []
        self.current_row = []

    def handle_starttag(self, tag, attrs):
        if tag == 'table': self.in_table = True
        elif tag == 'tr': self.in_row = True
        elif tag == 'td': 
            self.in_cell = True
            self.current_cell_data = ""

    def handle_data(self, data):
        if self.in_cell:
            self.current_cell_data += data

    def handle_endtag(self, tag):
        if tag == 'td':
            self.current_row.append(self.current_cell_data.strip())
            self.in_cell = False
        elif tag == 'tr':
            if self.current_row:
                self.rows.append(self.current_row)
            self.current_row = []
            self.in_row = False
        elif tag == 'table':
            self.in_table = False

##  Print function
    # 1. Fetch the HTML content
    # 2. Parse the HTML to extract table rows
    # 3. Identify column indices from the header (first row)
    # 4. Map coordinates to characters
    # 5. Print the grid (y-coordinates decrease from top to bottom)
    
def print_secret_message(url):
    # 1. Fetch the HTML content
    try:
        with urllib.request.urlopen(url) as response:
            html_content = response.read().decode('utf-8')
    except Exception as e:
        print(f"Failed to fetch document: {e}")
        return

    # 2. Parse the HTML to extract table rows
    parser = GoogleDocTableParser()
    parser.feed(html_content)
    data_rows = parser.rows

    if not data_rows:
        print("No data found.")
        return

    # 3. Identify column indices from the header (first row)
    headers = data_rows[0]
    try:
        x_idx = headers.index('x-coordinate')
        char_idx = headers.index('Character')
        y_idx = headers.index('y-coordinate')
    except ValueError:
        # Fallback if headers aren't exactly as expected
        x_idx, char_idx, y_idx = 0, 1, 2

    # 4. Map coordinates to characters
    grid = {}
    max_x = 0
    max_y = 0

    for row in data_rows[1:]:
        if len(row) < 3: continue
        try:
            x = int(row[x_idx])
            y = int(row[y_idx])
            char = row[char_idx]
            
            grid[(x, y)] = char
            max_x = max(max_x, x)
            max_y = max(max_y, y)
        except ValueError:
            continue

    # 5. Print the grid (y-coordinates decrease from top to bottom)
    for y in range(max_y, -1, -1):
        line = "".join(grid.get((x, y), " ") for x in range(max_x + 1))
        print(line)

# Example Usage:
# print_secret_message("https://docs.google.com/document/d/e/2PACX-1vTMOmshQe8YvaRXi6gEPKKlsC6UpFJSMAk4mQjLm_u1gmHdVVTaeh7nBNFBRlui0sTZ-snGwZM4DBCT/pub")