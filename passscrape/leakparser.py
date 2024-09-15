import hashlib
from urllib.parse import urlparse
import enchant
import logging
from langdetect import detect
import langdetect
"""
This class deals with the raw text of a potential leak, trying to check if there are credentials
inside of it
"""
class LeakParser:
    def __init__(self, passlist, seperators, ignore_list, ratio, any_pw=False):
        self.passlist = self.get_lines(passlist)
        self.seperators = seperators
        self.ignore_list = ignore_list
        self.ratio = ratio
        self.any_pw = any_pw
    """
    Takes a line to check if it resolves as an URL
    """
    def is_url(self, line):
        try:
            res = urlparse(line)
            return all([res.scheme, res.netloc])
        except AttributeError:
            return False
    """
    Uses langdetect to detect language of text. Defaults to en_US
    """
    def get_language(self, text):
        try:
            res = detect(text)
        except langdetect.lang_detect_exception.LangDetectException as e:
            logging.error("Text has no language!")
            return 'en_US'
        result = ''
        for lg in enchant._broker.list_languages():
            if lg == res:
                result = lg
                break
            elif res in lg:
                result = lg
                break
        if result == '':
            result = 'en_US'
        return result
    """
    Check if word is in words, increases count if it is
    """
    def word_in_words(self, word, words):
        found = False
        for w in words:
            if w["txt"] == word:
                w["count"] += 1
                found = True
        if not found and word != '' and word != '\n':
            words.append({
                "txt": word, 
                "count": 1,
                "is_pw": False
            })
        return words
    """
    Gets all the words in text and returns them.
    Skips newlines, empty words, URL
    """
    def get_words(self, text):
        seperators = self.seperators
        lines = text.split("\n")
        words = []
        for line in lines:
            if self.is_url(line) or line == '\n' or line == '':
                continue
            #words = self.word_in_words(line, words)
            wordsInLine = []
            if " " in line:
                for s in line.split(" "):
                    if s != '' and s != '\n':
                        wordsInLine.append(s)
            for word in wordsInLine:
                for sep in seperators:
                    if sep in word:
                        for s in word.split(sep): 
                            if s != '' and s != '\n':
                                words = self.word_in_words(s, words)
                                wordsInLine.append(s)        
                words = self.word_in_words(word, words)
        return words
    """
    Gets the language of text, counts the amount of words from dict and passwords, then decides if it is a leak 
    """
    def has_credentials(self, text):
        words = []
        lang = self.get_language(text)
        d = enchant.Dict(lang)
        pw_count = 0
        words = self.get_words(text)
        dict_count = 0
        word_count = 0
        for word in words:
            # Create sha1 hash of word because the password list is also hashes
            hexxed = hashlib.sha1(word["txt"].encode()).hexdigest()
            # Checks if the word is in the created dictionary and also if it is not a digit
            if d.check(word["txt"]) and not word["txt"].isdigit():
                dict_count += word["count"]
            # Skip words that are only 1 character, make sure the hexxes match, ignore false positives
            if (hexxed.upper() in self.passlist or hexxed in self.passlist) and word["txt"] not in self.ignore_list and len(word["txt"]) != 1:
                pw_count += word["count"]
                word["is_pw"] = True
            word_count += word["count"]
        logging.info(f'pw_count: {pw_count}, dict_count: {dict_count}, ratio: {pw_count/dict_count if dict_count != 0 else 0}')
        # No words in text
        if len(words) == 0:
            return False, words
        if self.any_pw and pw_count > 0:
            return True, words
        elif (dict_count > pw_count  and dict_count/word_count > 0.2 and pw_count/dict_count < self.ratio) or pw_count == 0: 
            print(f'Has no leaks, PWs: {pw_count}, Ws in dict: {dict_count}, ratio dict/numwords: {0 if word_count == 0 else dict_count/word_count}, num words: {word_count}, ratio {0 if dict_count == 0 else pw_count/dict_count}, top3: {sorted(words, key=lambda d: d["count"], reverse=True)[0:3]}')
            return False, words
        else:
            words_are_pw = [w for w in words if w['is_pw'] == True]
            print(f'Has leaks, PWs: {pw_count}, Ws in dict: {dict_count}, ratio dict/numwords: {dict_count/len(words)}, num words: {len(words)}, ratio {0 if dict_count == 0 else pw_count/dict_count}, pws: {words_are_pw}')
            return True, words
    
    """
    Get all the lines from text
    """
    def get_lines(self, filename):
        with open(filename, 'r') as f:
            return f.read().splitlines()