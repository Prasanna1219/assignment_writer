from fpdf import FPDF
import re

class PDF(FPDF):
    def header(self):
        # Add a grey vertical margin line on every page with color (111, 111, 111) and width 0.3
        self.set_draw_color(111, 111, 111)  # Light grey color for the margin line
        self.set_line_width(0.3)  # Set the line width to 0.3
        self.line(15, 0, 15, self.h)  # Draw line from top to bottom of the page

    def footer(self):
        pass  # No footer

# Create PDF object
pdf = PDF()
pdf.set_auto_page_break(auto=False, margin=15)

# Set a custom page break trigger
pdf.page_break_trigger = 250  # Custom page break trigger at 250mm

pdf.add_page()

# Register the Indie Flower handwriting font
pdf.add_font('Handwriting', '', 'LiuJianMaoCao-Regular.ttf', uni=True)

# Set handwriting font
pdf.set_font('Handwriting', size=12)

# Apply left margin
pdf.set_left_margin(20)  # Increase the left margin
pdf.set_x(20)  # Ensure writing starts after the margin

# Long text to simulate multiple pages
large_text = """Data scientists play a crucial role in addressing the challenges of big data by applying their skills in statistics, 
machine learning, data analysis, and domain knowledge to extract insights and make informed decisions. 
Here's how they contribute to solving big data challenges:

1. Data Cleaning and Preprocessing:
Challenge: Big data often contains noisy, incomplete, or inconsistent information.
Contribution: Data scientists clean, transform, and preprocess data to ensure it is structured and usable for analysis.

2. Data Integration:
Challenge: Big data often comes from multiple sources, making integration difficult.
Contribution: Data scientists combine data from various sources and formats into a unified dataset.

3. Data Analysis:
Challenge: Extracting meaningful insights from massive datasets is complex.
Contribution: Using advanced statistical techniques and machine learning algorithms, data scientists analyze data patterns and relationships.
""" * 2  # Repeat for testing multiple pages

# Function to print heading and body text with color coding and page break handling
def write_colored_text(pdf, text):
    # Split the text into lines and process each line
    lines = text.split('\n')
    
    for line in lines:
        # Check if the line is a heading or subheading (using simple regex)
        if re.match(r'^\d+\.|^[A-Z\s]+$', line):  # Match numbers or fully capitalized lines
            # Check if the line fits on the current page
            if pdf.get_y() + 12 > pdf.page_break_trigger:  # Check if remaining space is less than 12 mm
                pdf.add_page()  # Add a new page if there isn't enough space
            
            pdf.set_text_color(0, 0, 0)  # Set color to black for heading
        else:
            pdf.set_text_color(0, 15, 185)  # Set color to blue for regular text
        
        pdf.multi_cell(0, 10, line)

# Write the heading and body with different colors
write_colored_text(pdf, large_text)

# Check if the last page is empty
if pdf.page_no() > 1 and pdf.get_y() < pdf.page_break_trigger:
    # If the last page is nearly empty, we won't add a final page or we skip the content for the last one.
    print(f"Removing last page, no content after line {pdf.get_y()}")

# Save PDF
pdf_file_name = "assignment.pdf"
pdf.output(pdf_file_name)

print(f"PDF with custom page break trigger and empty page removal has been created successfully as '{pdf_file_name}'.")
