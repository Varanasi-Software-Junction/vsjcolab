# -*- coding: utf-8 -*-
"""OCR Reader.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1giRMQRQhXTtldXMbYFjInRLnlXaftKWp

**Program to use pytesseract for OCR reading**
[pytesseract](https://pypi.org/project/pytesseract/) is a wrapper for  Google’s Tesseract-OCR Engine whose documentation is at
[Tesseract-OCR Engine](https://github.com/tesseract-ocr/tesseract)

We will read the text from a picture stored on your hard disk and of a picture taken from your laptop's web camera.
"""

!sudo apt install tesseract-ocr # sudo permits a user to execute a command as a super user
# apt is short for Advance Packing Tool which extracts a package from a library.
!pip install pytesseract
# Our application requires pytesseract which has tesseract-ocr as a dependency

import pytesseract
from PIL import Image

"""IPython display is a module of the IPython library and their respective libraries are at

[ipython.readthedocs.io/en/stable/](https://ipython.readthedocs.io/en/stable/)
and
[IPython.display](https://ipython.readthedocs.io/en/stable/api/generated/IPython.display.html#IPython.display.display)

In particular we wil use the display function whose usage is:

local_file = FileLink("my/data.txt")

display(local_file)

The documentation for the Javascript class is at [Javascript](https://ipython.readthedocs.io/en/stable/api/generated/IPython.display.html#IPython.display.Javascript)
it takes a string as input and creates a javascript object.

[Base64](https://docs.python.org/3/library/base64.html)
provides functions for encoding binary data to printable ASCII characters and decoding such encodings back to binary data. It provides encoding and decoding functions for the encodings specified in RFC 4648, which defines the Base16, Base32, and Base64 algorithms, and for the de-facto standard Ascii85 and Base85 encodings.

Link to eval_js  [documentation](https://colab.research.google.com/notebooks/snippets/advanced_outputs.ipynb#scrollTo=MprPsZJa3AQF).



The code in the next block is inspired by
[Web Camera Javascript](https://colab.research.google.com/notebooks/snippets/advanced_outputs.ipynb#scrollTo=buJCl90WhNfq&line=1&uniqifier=1).

"""

from IPython.display import display, Javascript
 
from google.colab.output import eval_js
from base64 import b64decode

def clickPic(filename='photo.jpg', quality=0.8):
  js = Javascript('''
    async function clickPicJS(quality) {
      const div = document.createElement('div');
      const capture = document.createElement('button');
      capture.textContent = 'Press to Capture';
      div.appendChild(capture);

      const video = document.createElement('video');
      video.style.display = 'block';
      const stream = await navigator.mediaDevices.getUserMedia({video: true});

      document.body.appendChild(div);
      div.appendChild(video);
      video.srcObject = stream;
      await video.play();

      // Resize the output to fit the video element.
      google.colab.output.setIframeHeight(document.documentElement.scrollHeight, true);

      // Wait for Capture to be clicked.
      await new Promise((resolve) => capture.onclick = resolve);

      const canvas = document.createElement('canvas');
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      canvas.getContext('2d').drawImage(video, 0, 0);
      stream.getVideoTracks()[0].stop();
      div.remove();
      return canvas.toDataURL('image/jpeg', quality);
    }
    ''')
  display(js)
  data = eval_js('clickPicJS({})'.format(quality))
  binary = b64decode(data.split(',')[1])
  with open(filename, 'wb') as f:
    f.write(binary)
  return filename

from IPython.display import Image as img
try:
  filename = clickPic()
  print('Saved to {}'.format(filename))
  imgpath=filename
  # Show the image which was just taken.
  display(img(filename))
except Exception as err:
  # Errors will be thrown if the user does not have a webcam or if they do not
  # grant the page permission to access it.
  print(str(err))

from google.colab import files
uploaded = files.upload()
print(uploaded)
keys=list(uploaded.keys())
print(keys[0])
imgpath=keys[0]

print(imgpath)
readtext = pytesseract.image_to_string(Image.open(imgpath))
print(readtext)
pdf = pytesseract.image_to_pdf_or_hocr(imgpath, extension='pdf')
with open('extracteddata.pdf', 'w+b') as f:
    f.write(pdf) # pdf type is bytes by default