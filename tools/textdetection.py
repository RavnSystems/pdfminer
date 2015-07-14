#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 13 12:43:18 2015

@author: janvh
"""
import json
import sys
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFConverter
from pdfminer.pdfpage import PDFPage
from pdfminer.layout import LTContainer
from pdfminer.layout import LTText

class TextDetector(PDFConverter):

    def __init__(self, rsrcmgr):
        PDFConverter.__init__(self, rsrcmgr, None, codec='utf-8', pageno=1, laparams=None)
        self.pages = {}
        return

    def receive_layout(self, ltpage):
        def render(item):
            if isinstance(item, LTContainer):
                for child in item:
                    ret = render(child)
                    if ret:
                        return True
            elif isinstance(item, LTText):
                return len(item.get_text()) > 0
            return False

        ret = render(ltpage)
        self.pages[ltpage.pageid] = ret
        return

    # Some dummy functions to save memory/CPU when all that is wanted
    # is text.  This stops all the image and drawing ouput from being
    # recorded and taking up RAM.
    def render_image(self, name, stream):
        return

    def paint_path(self, gstate, stroke, fill, evenodd, path):
        return


def main(argv):
    import getopt
    def usage():
        print ('usage: %s [-a]'
               ' file ...' % argv[0])
        return 100
    try:
        (opts, args) = getopt.getopt(argv[1:], 'dp:m:P:o:CnAVM:L:W:F:Y:O:R:St:c:s:')
    except getopt.GetoptError:
        return usage()
    if not args:
        return usage()

    rsrcmgr = PDFResourceManager(caching=True)
    device = TextDetector(rsrcmgr)
    for fname in args:
        fp = file(fname, 'rb')
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        #for page in PDFPage.get_pages(fp, pagenos,
        #                              maxpages=maxpages, password=password,
        #                              caching=caching, check_extractable=True):
        for page in PDFPage.get_pages(fp, caching=True, check_extractable=False):
            #page.rotate = (page.rotate+rotation) % 360
            interpreter.process_page(page)
        fp.close()
    device.close()
    print(json.dumps(device.pages))

    return 0

if __name__ == '__main__':
    #argv = ['textdetection.py', '../../Data/banking/notext.pdf']
    #main(argv)
    sys.exit(main(sys.argv))
