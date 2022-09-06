class VocabularyModal:
    """Vocabulary Modal is a customer note type in Anki.
    It contains the following fields:
    - Word: The word to be learned
    - Context: The context of the word
    - Context Audio: The audio of the context
    - Meaning: The meaning of the word
    - Chinese: The Chinese translation of the word
    - Soundmark: The soundmark of the word
    - Pronunciation Audio: The audio of the word
    """
    def __init__(self, fields: dict):
        self.word = fields.get('word', None)
        self.context = fields.get('context', None)
        self.context_audio = fields.get('context_audio', None)
        self.meaning = fields.get('meaning', None)
        self.chinese = fields.get('chinese', None)
        self.soundmark = fields.get('soundmark', None)
        self.pronunciation_audio = fields.get('pronunciation_audio', None)

