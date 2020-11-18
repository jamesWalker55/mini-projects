# mini-projects

## pdfimg.py

```
Usage: pdfimg.py [file] [Option]
Option: 0 - Rough convert every page
        1 - Create folder and extract raw images from each page
```

A command line utility that gets images from PDF files.

It can either extract the raw images from the PDF, or convert each page to images individually.


## Liked-dl

I don't trust YouTube and neither should you.

This script downloads every video from a playlist as audio. It adds a `date` tag to all downloaded files. (This assumes that output files will be opus audio)

This script is intended to be used for downloading my Liked Videos playlist. YouTube changed every users' Liked Videos playlist to private, so I needed to access the YouTube API to access the playlist with youtube-dl, hence this script was created.

## rectangle-packing

This takes an input directory of `*.png` images, and tries to fit them in a single bigger image.

Edit the settings directly in the `packer.py` file:

- `path`: Input directory of images
- `outpath`: Output directory
- `mw`: Width multiplier, controls available space in output image. Calculated with `1920*mw`
- `mh`: Height multiplier, controls available space in output image. Calculated with `1080*mh`
