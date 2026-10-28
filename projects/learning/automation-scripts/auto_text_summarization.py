
# Install first: pip install nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

def summarize_text(text):
    stop_words = set(stopwords.words("english"))
    words = word_tokenize(text)
    freq_table = dict()

    for word in words:
        word = word.lower()
        if word in stop_words:
            continue
        freq_table[word] = freq_table.get(word, 0) + 1

    sentences = sent_tokenize(text)
    sentence_scores = dict()

    for sent in sentences:
        for word in freq_table:
            if word in sent.lower():
                sentence_score[sent] = sentence_scores.get(sent, 0) + freq_table[word]
        
    summary = " ".join([sentence for sentence in sentences if sentence_scores.get(sentence, 0) > 1])

    print(summary)

sample_text = "Python is a powerful tool for automating tasks. This script provides a quick overview of text summarization."

summarize_text(sample_text)

