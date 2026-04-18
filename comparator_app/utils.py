import difflib
import re
from io import BytesIO

from docx import Document
from PyPDF2 import PdfReader


TOKEN_RE = re.compile(r"\w+|[^\w\s]|\n")
SENTENCE_RE = re.compile(r"[.!?]+")


def extract_text(uploaded_file):
    ext = uploaded_file.name.rsplit('.', 1)[-1].lower()
    file_bytes = uploaded_file.read()

    if ext == 'txt':
        return file_bytes.decode('utf-8', errors='ignore')

    if ext == 'docx':
        doc = Document(BytesIO(file_bytes))
        return '\n'.join(paragraph.text for paragraph in doc.paragraphs)

    if ext == 'pdf':
        reader = PdfReader(BytesIO(file_bytes))
        return '\n'.join(page.extract_text() or '' for page in reader.pages)

    return ''


def text_stats(text):
    words = re.findall(r"\b\w+\b", text)
    sentences = [s for s in SENTENCE_RE.split(text) if s.strip()]
    return {
        'word_count': len(words),
        'sentence_count': len(sentences),
        'character_count': len(text),
    }


def similarity_percent(left_text, right_text):
    ratio = difflib.SequenceMatcher(None, left_text, right_text).ratio()
    return round(ratio * 100, 2)


def tokenize(text):
    return TOKEN_RE.findall(text)


def highlight_html(tokens, opcodes, side='left'):
    html_parts = []
    for tag, i1, i2, j1, j2 in opcodes:
        if side == 'left':
            chunk = tokens[i1:i2]
            if tag in ('delete', 'replace'):
                cls = 'removed' if tag == 'delete' else 'changed'
                html_parts.append(f'<span class="{cls}">{escape_html(join_tokens(chunk))}</span>')
            elif tag == 'equal':
                html_parts.append(escape_html(join_tokens(chunk)))
        else:
            chunk = tokens[j1:j2]
            if tag in ('insert', 'replace'):
                cls = 'added' if tag == 'insert' else 'changed'
                html_parts.append(f'<span class="{cls}">{escape_html(join_tokens(chunk))}</span>')
            elif tag == 'equal':
                html_parts.append(escape_html(join_tokens(chunk)))
    return ''.join(html_parts).replace('\n', '<br>')


def build_diff(left_text, right_text):
    left_tokens = tokenize(left_text)
    right_tokens = tokenize(right_text)
    matcher = difflib.SequenceMatcher(None, left_tokens, right_tokens)
    opcodes = matcher.get_opcodes()
    return {
        'left_html': highlight_html(left_tokens, opcodes, side='left'),
        'right_html': highlight_html(right_tokens, opcodes, side='right'),
    }


def join_tokens(tokens):
    output = []
    for token in tokens:
        if not output:
            output.append(token)
            continue

        if token in {'.', ',', ';', ':', '!', '?', ')', ']', '}'}:
            output.append(token)
        elif output[-1] in {'(', '[', '{', '\n'}:
            output.append(token)
        elif token == '\n':
            output.append('\n')
        else:
            output.append(' ' + token)
    return ''.join(output)


def escape_html(value):
    return (
        value.replace('&', '&amp;')
        .replace('<', '&lt;')
        .replace('>', '&gt;')
    )
