import os
import requests
import json
import re
import string

class MerriamWebster:
    def __init__(self, api_key) -> None:
        self.api_key = api_key
    
    def __get_pronunciation_media_url(audio):
        language_code = 'en'
        country_code = 'us'
        format = 'mp3'
        subdirectory = ''
        base_file = audio
        
        # calculate subdirectory
        if audio.startswith('bix'):
            subdirectory = 'bix'
        elif audio.startswith('gg'):
            subdirectory = 'gg'
        elif re.match('^[0-9]|[{}]'.format(string.punctuation), audio) is not None:
            subdirectory = 'number'
        else:
            subdirectory = audio[0]

        url = f'https://media.merriam-webster.com/audio/prons/{language_code}/{country_code}/{format}/{subdirectory}/{base_file}.{format}'
        return url
    
    def request_word_info(self, word):
        endpoint = f'https://dictionaryapi.com/api/v3/references/collegiate/json/{word}?key={self.api_key}'
        response = requests.get(endpoint).json()
        return response

    def get_pronunciation(self, word):
        """Get the pronunciation of the word
        Return soundmark and audio url
        """
        data = self.request_word_info(word)
        if len(data) == 0:
            return None, None
        
        if 'meta' not in data[0] or word.lower() != data[0]['meta']['id'].lower():
            return None, None

        data = data[0]
        
        if 'hwi' not in data or 'prs' not in data['hwi']:
            return None, None

        sound_data = data['hwi']['prs'][0]
        soundmark = sound_data['mw']
        audio = sound_data['sound']['audio']
        audio_url = MerriamWebster.__get_pronunciation_media_url(audio)
        return soundmark, audio_url
