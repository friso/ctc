ctc
===

Cut the Crap (TM)

Result of a hack session that resulted in [this](http://agile-stream-1480.herokuapp.com/static/client.html "Cut the Crap"). Far from done, but slightly functional.

The idea is:
1. Paste long text into the text box.
2. Hit the 'CUT' button.
3. Look at the words that it show; this is what the text is really about. The rest is crap.

The method is a simple TF-IDF, where we pre-fill the document frequency table by seeding it using a part of the Open American National Corpus (next update will use the entire thing).

TODOs:
- Use Redis for storing frequencies instead of a Python dict, such that it scales to a larger corpus.
- Use entire OANC to pre-populate the doc frequency table.
- Update the doc frequency table with user input.
- Do language detection on the input to reject non Enlgish text, as it will probably mess up the frequency tables.


