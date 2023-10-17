import streamlit as st
import base64
from fpdf import FPDF

img_path = "AC.jpg"
st.image(img_path, channels='BGR')

import base64

with open(img_path, "rb") as img_file:
    b64_string = base64.b64encode(img_file.read()).decode()

background = f'''
    <style>
    body {{
        background-image: url("data:image/jpeg;base64,{b64_string}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        background-position: center;
    }}
    #root, #MainMenu, .element-container{{
        background: transparent !important;
    }}
    </style>
'''

st.markdown(background, unsafe_allow_html=True)



def classify_sequence(sequence, species):
    # Placeholder for your classification logic
    # Replace with your actual classification logic
    return f"Result: The given DNA sequence belongs to species X"

# Initialize session state variables if they don't exist
if 'pdf_output' not in st.session_state:
    st.session_state['pdf_output'] = None

st.title("NucleoVet 🦠")
st.write("This app enables classification of species based on their DNA sequence.")

study_name = st.text_input("Study Name:")
study_date = st.date_input("Study Date:")
study_time = st.time_input("Study Time:")

species_options = ["Virus", "Bacteria", "Fungus"]
selected_species = st.selectbox("Select Specie:", species_options)

uploaded_file = st.file_uploader("Choose a DNA sequence file", type=["txt", "fasta"])

if uploaded_file:
    dna_sequence = uploaded_file.read().decode()
    st.text_area("DNA Sequence:", value=dna_sequence, height=200, max_chars=None)
else:
    dna_sequence = st.text_input("Or Enter DNA Sequence:")

if st.button("Classify this Sequence"):
    result = classify_sequence(dna_sequence, selected_species)
    st.write(result)

    pdf = FPDF()
    pdf.add_page()

    # Set font for company title
    pdf.set_font("Arial", 'B', 16)  # 'B' argument specifies bold
    
    # Calculate width of text to center it
    company_title = "Company Name"
    title_width = pdf.get_string_width(company_title) + 6  # +6 for a little padding
    page_width = 210  # A4 width in mm
    x_position = (page_width - title_width) / 2  # calculate x position to center text
    
    pdf.set_xy(x_position, 10)  # Set x and y position for title
    pdf.cell(title_width, 10, txt=company_title, ln=True, align='C')  # Centered company title

    pdf.set_font("Arial", size=12)  # Set font back to normal for rest of PDF
    pdf.cell(200, 10, txt=f"Study Name: {study_name}", ln=True)
    pdf.cell(200, 10, txt=f"Study Date: {study_date.strftime('%Y-%m-%d')}", ln=True)
    pdf.cell(200, 10, txt=f"Study Time: {study_time.strftime('%H:%M:%S')}", ln=True)
    pdf.cell(200, 10, txt=f"Selected Specie: {selected_species}", ln=True)
    pdf.cell(200, 10, txt=f"DNA Sequence: {dna_sequence}", ln=True)
    pdf.cell(200, 10, txt=result, ln=True)
    
    st.session_state['pdf_output'] = pdf.output(dest='S').encode('latin')

    b64 = base64.b64encode(st.session_state['pdf_output']).decode()
    href = f'<a href="data:application/pdf;base64,{b64}" download="classification_result.pdf">Download Classification Result</a>'
    st.markdown(href, unsafe_allow_html=True)
