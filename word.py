class Word:
    def __init__(self, word):
        self.word = word

    def set_pronunciation(self, pronunciation):
        self.pronunciation = pronunciation
    
    def set_pronunciation_media(self, pronunciation_media):
        self.pronunciation_media = pronunciation_media

    def get_word(self):
        return self.word

    def get_pronunciation(self):
        return self.pronunciation

    def get_pronunciation_media(self):
        return self.pronunciation_media