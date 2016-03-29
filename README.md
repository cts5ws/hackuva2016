# Story Time

***This project was submitted to HackUVA and won the best desktop hack award.***

We thought we could mimic creativity in a computer. The input is an image in some URL. The output is a few lines of text about the image. The end goal is to have some sort of fictional story about the image. Applications include recreational use, creating stories on the fly for entertainment; parents could use it for young children; this project is more a proof-of-concept.

The steps are below.
1. Find tags associated with input image
2. Assign tags to parts of speech
3. Create a grammar of English language
4. Use n-gram analysis to output some text

We use a few different tools. The project is wrapped in a Django framework (Python backend) and the frontend is Bootstrap. We use *claif.ai* for tagging images, the *nltk* package for Python for assigning tags to categories and working with grammars. We use n-grams (particularly 2-gram) from the [Corpus of Contemporary American English](http://www.ngrams.info/intro.asp).

We'll be expanding on this project.
- Although tags are fairly accurate, we need more verbs (convert nouns to related verbs?)
- We can use more complicated grammar (e.g. include prepositional phrases)
- Changing, or adding, more n-gram analysis (greater than 2) can result in more realistic sentences
- For story flow, use the object of the previous sentence as the subject of the next
- Get data by user "yays" and "nays" regarding the output and learn
- Use tensorflow for neural network and language modeling

Technical issues:
- Static files in Django


Contact: [Srikanth Chelluri](mailto:sc5ba@virginia.edu), [Nikhil Gupta](mailto:ng3br@virginia.edu), [Cole Schafer](mailto:cts5ws@virginia.edu)
