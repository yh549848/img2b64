#! /usr/bin/env python

"""
Replace img src in HTML with base64 encoded string

Usage:
  img2b64 <html>

Options:
  <html> : Input HTML

"""

import os
import base64

from docopt import docopt
from bs4 import BeautifulSoup


def relpath2abspath(relpath, root_dir):
    # NOTE: Encode local src only
    if relpath.startswith('http'):
        return relpath

    if relpath.startswith('/') or relpath.startswith('\\'):
        if os.path.exists(relpath):
            return relpath

    abspath = os.path.join(root_dir, relpath)

    return abspath

def main():
    options = docopt(__doc__)
    html_path = options['<html>']

    with open(html_path) as f:
        html_doc = BeautifulSoup(f.read(), 'html.parser')

    root_dir = os.path.dirname(html_path)
    img_tags = html_doc.find_all('img')
    def_img_data_scheme = "data:image/{};base64,"

    for t in img_tags:
        src_attr = t.attrs['src']
        img_path = relpath2abspath(src_attr, root_dir)

        try:
            with open(img_path, 'rb') as f:
                img_b64 = base64.b64encode(f.read())
        except FileNotFoundError:
            continue
        else:
            ext = img_path.split('.')[-1].lower()

            # NOTE: The data URI must match the MIME type
            ext = 'jpeg' if ext == 'jpg' else ext

            t.attrs['src'] = ''.join([def_img_data_scheme.format(ext), img_b64.decode('utf-8')])

    print(html_doc)


if __name__ == '__main__':
    main()
