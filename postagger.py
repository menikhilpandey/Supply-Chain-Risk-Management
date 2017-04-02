import nltk

def noun_extractor(text):
    
    tokenize_text = nltk.word_tokenize(text)
    tag_sequence =  nltk.pos_tag(tokenize_text)
    #print tag_sequence
    noun_list = [item[0] for item in tag_sequence if item[1].startswith("N")]
    #print (' ').join(noun_list)
    return (' ').join(noun_list)

# text = "We are going out. Just you and me."
# print     noun_extractor(text)
