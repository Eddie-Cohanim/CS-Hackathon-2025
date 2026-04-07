from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

def fix_word_ultimate_rtl(file_path, output_path):
    doc = Document(file_path)
    
    for paragraph in doc.paragraphs:
        if not paragraph.text.strip():
            continue
            
        # 1. יישור הפסקה לימין
        paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        
        # 2. הגדרת הפסקה כולה מימין לשמאל (RTL Paragraph)
        pPr = paragraph._element.get_or_add_pPr()
        bidi = OxmlElement('w:bidi')
        bidi.set(qn('w:val'), '1')
        pPr.append(bidi)
        
        # 3. הגדרת כל חלקיק טקסט (Run) כ-RTL - זה מה שמונע מהאנגלית לשבור את המשפט
        for run in paragraph.runs:
            rPr = run._element.get_or_add_rPr()
            rtl = OxmlElement('w:rtl')
            rtl.set(qn('w:val'), '1')
            rPr.append(rtl)

    doc.save(output_path)
    print(f"הקובץ תוקן ונשמר ב: {output_path}")

# שים פה את הנתיב לקובץ *המקורי* מהאייג'נט
input_file = "צוות_סיעודי_אחיות_נוהל_מניעת_אספירציה_בזמן_ארוחו_Procedure.docx"  
output_file = "צוות_סיעודי_אחיות_נוהל_מניעת_אספירציה_בזמן_ארוחו_Procedure_fixed.docx"
fix_word_ultimate_rtl(input_file, output_file)