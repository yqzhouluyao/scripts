import os
import sys
from warcio.archiveiterator import ArchiveIterator
import requests
from urllib.parse import urlparse

def main():
    if len(sys.argv) != 3:
        print("Usage: python extract_warc.py input_warc_file output_directory")
        sys.exit(1)

    input_warc_file = sys.argv[1]
    output_directory = sys.argv[2]

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    with open(input_warc_file, 'rb') as stream:
        for record in ArchiveIterator(stream):
            if record.rec_type == 'response':
                url = record.rec_headers.get_header('WARC-Target-URI')
                parsed_url = urlparse(url)

                # Remove leading '/' from the path
                path = parsed_url.path.lstrip('/')
                if not path:
                    path = "index.html"

                # Create the output file path
                output_file = os.path.join(output_directory, path)

                # Ensure the directory exists
                os.makedirs(os.path.dirname(output_file), exist_ok=True)

                with open(output_file, 'wb') as f:
                    f.write(record.content_stream().read())

if __name__ == '__main__':
    main()
