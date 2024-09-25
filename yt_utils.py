import spacy
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import en_core_web_sm

# Load the spaCy English language model
nlp = spacy.load("en_core_web_sm")
# nlp = en_core_web_sm.load()

# Initialize the Porter Stemmer
ps = PorterStemmer()

def passWord(token):
  if token.ent_type_ == "PERSON":
      return False 
  elif token.ent_type_ == "DATE" or ("Num" in str(token.morph) and token.ent_type_ == ""):
      return False 
  elif token.pos_ == "AUX" :
      return False 
  elif token.dep_ == "punct" or token.dep_ == "prep":
      return False

  return True
def passWord_title(token):
  if token.ent_type_ == "DATE" or ("Num" in str(token.morph) and token.ent_type_ == ""):
      return False 
  elif token.pos_ == "AUX" :
      return False 
  elif token.dep_ == "punct" or token.dep_ == "prep":
      return False

  return True


barred_words = {'shorts', '#shorts'}
def passWord_sub(token, clip_type):
    if clip_type == "shorts" and token.text.lower() in barred_words:
        return False 
    return True
def extract_important_words_subjects(sentence, clip_type, curr_search):
    # Process the input sentence using spaCy
    doc = nlp(sentence)

    # Extract descriptive words by filtering out named entities (persons) and keeping adjectives and nouns
    # descriptive_words = [ps.stem(token.text) for token in doc if (token.ent_type_ != "PERSON" and token.ent_type_ != "DATE" and token.ent_type_ != "")]

    # # Extract noun chunks (important words) from the processed sentence
    
    important_words = [token.text.lower() for token in doc.noun_chunks if (passWord_sub(token, clip_type) and token.text.lower() != curr_search)] # if passWord_title(token)]
    hints = [token.text.lower() for token in doc.sents if (passWord_sub(token, clip_type) and token.text.lower() != curr_search)]

    return list(set(important_words + hints))


def extract_important_words_entities(sentence, clip_type):
    # Process the input sentence using spaCy
    doc = nlp(sentence)

    # Extract descriptive words by filtering out named entities (persons) and keeping adjectives and nouns
    ## ent - entity
    descriptive_words = [ps.stem(token.text.lower()) for token in doc if passWord(token)]

    # # Extract noun chunks (important words) from the processed sentence
    # important_words = [chunk.text for chunk in doc.noun_chunks]

    return list(set(descriptive_words))