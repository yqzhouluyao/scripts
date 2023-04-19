import openai
from ebooklib import epub
from lxml import html
import ebooklib

# Set up your OpenAI API key
openai.api_key = ""

def read_epub(file_path):
    book = epub.read_epub(file_path)
    items = []
    for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
        items.append(item)
    return book, items

def translate_text(text, source_lang, target_lang):
    MAX_TOKENS = 4096
    translated_text = ''
    
    prompt = f"Translate the following text from {source_lang} to {target_lang}:\n\n"
    tokens_to_reserve = len(prompt) + 200 # Reserve tokens for the prompt and some extra space
    
    while text:
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt + text[:MAX_TOKENS - tokens_to_reserve],
            max_tokens=MAX_TOKENS - tokens_to_reserve,
            n=1,
            stop=None,
            temperature=0.8,
        )

        translated_chunk = response.choices[0].text.strip()
        translated_text += translated_chunk
        text = text[MAX_TOKENS - tokens_to_reserve:]

    return translated_text




def translate_item(item):
    content = item.content.decode('utf-8')
    content = content.replace('<?xml version="1.0" encoding="utf-8"?>', '') # Remove the XML declaration
    content = content.encode('utf-8') # Encode content back to bytes
    root = html.fromstring(content)
    paragraphs = root.xpath('//p')
    
    for paragraph in paragraphs:
        text = paragraph.text_content()
        translated_text = translate_text(text, 'English', 'Simplified Chinese')
        paragraph.text = translated_text

    return html.tostring(root, encoding='utf-8')

def extract_toc(book):
    toc = book.toc
    new_toc = []
    
    for entry in toc:
        if isinstance(entry, tuple):
            new_toc.append(epub.Link(entry[1], translate_text(entry[0], 'English', 'Simplified Chinese'), entry[2]))
        elif isinstance(entry, epub.Link):
            new_toc.append(epub.Link(entry.href, translate_text(entry.title, 'English', 'Simplified Chinese'), entry.uid))
        elif isinstance(entry, epub.Section):
            new_section = epub.Section(translate_text(entry.name, 'English', 'Simplified Chinese'))
            new_toc.append(new_section)
            new_section.subsections = extract_toc(entry)
    return new_toc

def save_epub(file_path, book):
    epub.write_epub(file_path, book)

def main(input_file, output_file):
    ebook, items = read_epub(input_file)

    translated_ebook = epub.EpubBook()
    translated_ebook.set_identifier(ebook.get_metadata('DC', 'identifier')[0][0])
    translated_ebook.set_title(ebook.get_metadata('DC', 'title')[0][0] + ' (Simplified Chinese)')
    translated_ebook.set_language('zh-CN')

    for author in ebook.get_metadata('DC', 'creator'):
        translated_ebook.add_author(author[0])

    for item in items:
        translated_content = translate_item(item)
        translated_item = epub.EpubHtml(title=item.title, file_name=item.file_name, lang='zh-CN')
        translated_item.set_content(translated_content)
        translated_ebook.add_item(translated_item)

    translated_toc = extract_toc(ebook)
    translated_ebook.toc = translated_toc

    save_epub(output_file, translated_ebook)

if __name__ == "__main__":
    input_file = "/epub/how-to-start-a-startup-a-yc-course.epub"
    output_file = "/epub/output/translated_ebook.epub"
    main(input_file, output_file)
