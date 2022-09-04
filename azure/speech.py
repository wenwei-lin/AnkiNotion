import azure.cognitiveservices.speech as speechsdk
from azure.cognitiveservices.speech import AudioDataStream

class AzureSpeech:
    def __init__(self, key, region) -> None:
        self.key = key
        self.region = region
        self.speech_config = speechsdk.SpeechConfig(subscription=self.key, region=self.region)
        self.speech_config.speech_synthesis_language = "en-US" 
        self.speech_config.speech_synthesis_voice_name = "en-US-ChristopherNeural"
        self.synthesizer = speechsdk.SpeechSynthesizer(speech_config=self.speech_config, audio_config=None)

    def synthesize_audio(self, text):
        """Synthesize audio from text.
        Returns a byte array of audio data.
        """
        result = self.synthesizer.speak_text_async(text).get()
        return result.audio_data
