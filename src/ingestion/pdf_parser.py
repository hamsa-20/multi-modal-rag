import fitz  # pymupdf
from pathlib import Path
from .image_ocr import ocr_image
from .table_extractor import extract_tables

def parse_pdf(path: str, out_dir: str):
    doc = fitz.open(path)
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    pages_meta = []
    for i in range(len(doc)):
        page = doc[i]
        text = page.get_text("text")
        imgs = page.get_images(full=True)
        image_files = []
        for img_index, img in enumerate(imgs):
            xref = img[0]
            pix = fitz.Pixmap(doc, xref)
            img_path = out / f"page{i+1}_img{img_index+1}.png"
            if pix.n < 5:
                pix.save(str(img_path))
            else:
                pix = fitz.Pixmap(fitz.csRGB, pix)
                pix.save(str(img_path))
            image_files.append(str(img_path))
            pix = None
        tables = extract_tables(path, i+1, out)
        images_ocr = {p: ocr_image(p) for p in image_files}
        pages_meta.append({
            "page": i+1,
            "text": text,
            "images": image_files,
            "images_ocr": images_ocr,
            "tables": tables
        })
    return pages_meta
