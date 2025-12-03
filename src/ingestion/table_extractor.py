# This is optional. If camelot not available, returns [].
from pathlib import Path
try:
    import camelot
except Exception:
    camelot = None

def extract_tables(pdf_path, page_no, out_dir):
    out = Path(out_dir)
    if camelot is None:
        return []
    try:
        tables = camelot.read_pdf(pdf_path, pages=str(page_no))
        out_files = []
        for idx, t in enumerate(tables):
            fname = out / f"page{page_no}_table{idx+1}.csv"
            t.to_csv(fname)
            out_files.append(str(fname))
        return out_files
    except Exception:
        return []
