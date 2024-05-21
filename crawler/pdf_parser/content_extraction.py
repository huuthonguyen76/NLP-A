import fitz
from .multi_column import column_boxes


def pdf_to_text(pdf_file_path: str) -> str:
    """
    Parse the PDF file to raw text
    """
    result = ""
    try:
        doc = fitz.open(pdf_file_path)
        for page in doc:
            # detect textboxes for multi-column file
            bboxes = column_boxes(page, footer_margin=50, no_image_text=True)
            for rect in bboxes:
                result += page.get_text(clip=rect, sort=True) + "\n"
    except Exception as e:
        print("--------- PDF To Text Error --------")
        print(e)
        print("-" * 20)

    return result

