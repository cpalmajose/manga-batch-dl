# manga-batch-dl
A small Python script to batch download chapters

Currently works with: 
- www.mangareader.net

How to use the script:

1. Provide the link of the manga of interest
   - ex. www.mangareader.net/ore-monogatari

2. Run the batchdownload.py into python interpreter using the link using
   the windows command line or unix terminal:
   - python "www.mangareader.net/ore-monogatari"

3. Files will be created using your HOME environment variable using the date
   of when the script was run.

   To find out what your HOME path using command line or terminal:
   - Windows: echo %HOMEPATH%
   - Unix   : echo ~ 
            echo $HOME


