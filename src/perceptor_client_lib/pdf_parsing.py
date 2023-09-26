import fitz
from fitz import Document, Page, Pixmap


def get_images_from_document_pages(file) -> list[bytes]:
    def get_image_from_page(page: Page):
        pix: Pixmap = page.get_pixmap(matrix=fitz.Identity, dpi=None,
                                      colorspace=fitz.csRGB, clip=None, alpha=True, annots=True)
        return pix.pil_tobytes(format="PNG")

    pdf_file: Document = fitz.open(file)
    with pdf_file:
        doc_pages: list[Page] = list(map(lambda i: pdf_file[i], range(len(pdf_file))))
        pages_images = map(get_image_from_page, doc_pages)
        return list(pages_images)
