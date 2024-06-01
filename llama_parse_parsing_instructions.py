# llama_parse_parse_instructions.py

# Parsing instructions for the "Manual de Procedimientos de Enfermería"

parsing_instructions = '''
The document titled "Manual de Procedimientos de Enfermería" is a comprehensive guide from the Caja Costarricense de Seguro Social, published in November 2014 with a next revision date in November 2018. It was authored by several medical professionals including Dra. Carmen Loaiza Madriz, Dra. Jacqueline Monge Medina, Dra. Maritza Solís Oviedo, and others. This manual covers a wide range of nursing procedures and is divided into multiple chapters and sections, each addressing different aspects of nursing care.

The manual includes:
1. Major sections labeled as "Capítulo" followed by a Roman numeral and a title.
2. Subsections identified by numeric headings (e.g., 1.1, 1.2).
3. Detailed procedural steps, often formatted as bullet points or numbered lists.
4. Tables summarizing procedural steps, measurements, and guidelines.
5. Definitions, abbreviations, and symbols related to nursing terms and procedures.

Instructions:
1. Extract the document metadata including title, authors, version, publication date, and next revision date.
2. Identify and parse major sections starting with "Capítulo" followed by a Roman numeral and the section title.
3. Within each section, identify and parse subsections formatted with numeric headings.
4. Capture the content under each subsection, preserving the structure of bullet points and numbered lists.
5. Extract tables, ensuring to capture the headers and content of each row.
6. Parse the definitions section, identifying terms and their corresponding descriptions.

Example parsed sections:
- "Capítulo I. Procedimientos Administrativos"
  - "1.1 Uso del expediente de salud": Detailed steps and guidelines for using health records.
  - "1.2 Notas de Enfermería: Modelo SOAPE": Description and procedure for nursing notes using the SOAPE model.
- "Capítulo II. Procedimientos de Higiene"
  - "2.1 Baño en cama": Steps for performing bed baths for patients.

Example parsed definitions:
- "Abducción: Movimiento de separación de un miembro respecto al cuerpo."
- "Abrasión: Erosión de la epidermis por raspadura o rozamiento; puede ocasionar una hemorragia localizada y posteriormente salida de líquido seroso."

Answer questions using the information in this manual and be precise.
'''