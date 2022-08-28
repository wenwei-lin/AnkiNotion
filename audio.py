import azure.cognitiveservices.speech as speechsdk

class AzureAudio:
    def __init__(self, key, region) -> None:
        self.key = key
        self.region = region
        self.speech_config = speechsdk.SpeechConfig(subscription=self.key, region=self.region)
        self.speech_config.speech_synthesis_language = "en-US" 
        self.speech_config.speech_synthesis_voice_name = "en-US-ChristopherNeural"
        self.audio_config = speechsdk.audio.AudioOutputConfig(filename="temp.wav")
        self.synthesizer = speechsdk.SpeechSynthesizer(speech_config=self.speech_config, audio_config=self.audio_config)

    def synthesize_audio(text):
        self.synthesizer.speak_text_async(text)