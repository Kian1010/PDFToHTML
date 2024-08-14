from pdfminer.high_level import extract_text,extract_pages
#For getting markdown/html
from pdfminer.layout import LTTextContainer, LTChar,LTTextLine
import tkinter as tk
from tkinter import filedialog

# Function to prompt user to select a PDF file
def select_pdf():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Select a PDF file",
        filetypes=(("PDF files", "*.pdf"), ("All files", "*.*"))
    )
    return file_path

#Pulls plaintext and writes into txt file.
def write_to_text(pdf):
    text = extract_text(pdf)
    with open('output.txt','w',encoding='utf-8') as output_file:
        output_file.write(text)

def print_html_output(pdf):
    html_output = []
    for page_layout in extract_pages(pdf):
        for element in page_layout:
            if isinstance(element, LTTextContainer):  # 'Container' for text blocks
                for text_line in element:  # loops over each line of the text
                    line_html = []
                    current_style = None # track current style i.e. bold/italic 
                    if isinstance(text_line, LTTextLine):  # Checking if it's a text line
                        for char in text_line:  # loops through characters in the line
                            if isinstance(char, LTChar):
                                # Check for bold / italic text
                                if 'Bold' in char.fontname:
                                    char_style = 'bold'
                                elif 'Italic' in char.fontname:
                                    char_style='italic'
                                #If style changes: close previous tag & open new one.
                                if char_style != current_style:
                                    if current_style == 'bold':
                                        line_html.append("</strong>")
                                    elif current_style == 'italic':
                                        line_html.append("</em>")

                                    if char_style == 'bold':
                                        line_html.append("<strong>")
                                    elif char_style == 'italic':
                                        line_html.append("<em>")
                                    
                                    current_style = char_style
                                
                                line_html.append(char.get_text())

                        # Close any open tags at the end of the line
                        if current_style == 'bold':
                            line_html.append("</strong>")
                        elif current_style == 'italic':
                            line_html.append("</em>")



                    html_output.append(''.join(line_html))
                html_output.append('<br>\n')  # New line for HTML
    return ''.join(html_output)

#writes to html instead, takes in the html content
def write_to_htmlfile(pdf):
    html_content = print_html_output(pdf)
    with open('output.html','w',encoding='utf-8') as output_file:
        output_file.write(html_content)


#TODO: Possibly make it loop through multiple PDF files, and save multiple outputs

# document variable, can be changed or recieved in other ways
pdf = select_pdf()

if pdf:
    #prints html output
    write_to_htmlfile(pdf)

    #prints text output
  #  write_to_text(pdf)
else:
    print('No PDF selected')


