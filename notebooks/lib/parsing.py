import hashlib, re
from pathlib import Path
from bs4 import BeautifulSoup
from pypdf import PdfReader

def extract_html(path):
    with open(path, encoding="utf-8", errors="ignore") as source_file:
        soup = BeautifulSoup(source_file.read(), "html.parser")
    for tag in soup(["script", "style", "nav", "footer", "header"]):
        tag.decompose()
    return soup.get_text(separator="\n", strip=True)

def extract_pdf(path):
    reader = PdfReader(path)
    return "\n".join(page.extract_text() or "" for page in reader.pages)

def extract(path):
    return extract_pdf(path) if Path(path).suffix.lower() == ".pdf" else extract_html(path)

def clean(text):
    text = re.sub(r"(?m)^(Page \d+|Confidential).*\n?", "", text)
    return re.sub(r"\n{3,}", "\n\n", text).strip()

def content_hash(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()
