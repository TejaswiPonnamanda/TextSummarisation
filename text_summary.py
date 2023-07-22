import spacy 
from spacy.lang.en.stop_words import STOP_WORDS 
from string import punctuation
from heapq import nlargest
text="""As the sun dipped below the horizon, the sky transformed into a canvas of vivid colors. Shades of pink, orange, and gold spread across the horizon, casting a warm glow over the landscape. The gentle breeze carried the scent of blooming flowers, creating a serene atmosphere. Birds chirped their final melodies of the day as they settled into their nests. The world seemed to slow down, and for a moment, all worries faded away. A feeling of tranquility washed over me as I gazed at the breathtaking scene before me. Nature's beauty was a reminder of life's simple pleasures. With each passing moment, the sky's colors deepened, captivating my senses. It was a magical moment, one that I wished could last forever."""

def summarizer(rawdocs):
    stopwords=list(STOP_WORDS)
    #print(stopwords)
    nlp=spacy.load("en_core_web_sm")
    doc=nlp(rawdocs)
    #print(doc)
    tokens=[token.text for token in doc]
    #print(tokens)
    word_freq={}
    for word in doc:
        if word.text.lower() not in stopwords and word.text.lower() not in punctuation:
            if word.text not in word_freq.keys():
                word_freq[word.text]=1
            else:
                word_freq[word.text]+=1
    #print(word_freq)
    max_freq=max(word_freq.values())
    #print(max_freq)
    for word in word_freq.keys():
        word_freq[word]=word_freq[word]/max_freq 
    #print(word_freq)
    sent_tokens=[sent for sent in doc.sents]
    #print(sent_tokens)
    sent_scores={}
    for sent in sent_tokens:
        for word in sent:
            if word.text  in word_freq.keys():
                if sent not in sent_scores.keys():
                    sent_scores[sent]=word_freq[word.text]
                else:
                    sent_scores[sent]+=word_freq[word.text]
    #print(sent_scores)
    select_len=int(len(sent_tokens)*0.3)
    #print(select_len)
    summary=nlargest(select_len,sent_scores,key=sent_scores.get)
    #print(summary)
    final_summary=[word.text for word in summary]
    summary=' '.join(final_summary)
    #print(text)
    #print("Length of original text",len(text.split(' ')))
    #print(summary)
    #print("Length of summary text",len(summary.split(' ')))
    return summary,doc,len(rawdocs.split(' ')),len(summary.split(' '))