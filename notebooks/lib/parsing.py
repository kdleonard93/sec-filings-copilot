import hashlib, re
from pathlib import Path
from bs4 import BeautifulSoup
from pypdf import PdfReader

def extract_html(path):
    with open(path, encoding="utf-8", errors="ignore") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
    for tag in soup(["script", "style", "nav", "footer", "header"]):
        tag.decompose()
    return soup.get_text(separator="\n", strip=True)   # keep line breaks

def extract_pdf(path):
    reader = PdfReader(path)                           # UC Volume path works as-is
    return "\n".join(page.extract_text() or "" for page in reader.pages)

def extract(path):
    return extract_pdf(path) if Path(path).suffix.lower() == ".pdf" else extract_html(path)

def clean(t):
    t = re.sub(r"(?m)^(Page \d+|Confidential).*\n?", "", t)   # headers/footers
    return re.sub(r"\n{3,}", "\n\n", t).strip()

def content_hash(t):
    return hashlib.sha256(t.encode("utf-8")).hexdigest()
