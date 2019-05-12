#!/usr/bin/env python


import argparse
import io
from Config import AUDIO_CONFIG


def transcribe_file(speech_file):
    """Transcribe the given audio file."""
    from google.cloud import speech_v1p1beta1 as speech
    from google.cloud.speech_v1p1beta1 import enums
    from google.cloud.speech_v1p1beta1 import types
    from google.cloud import translate as translate
    from google.cloud import texttospeech
    import os

    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.getenv("HOME")+"/gspeech.json"


    client = speech.SpeechClient()
    translate_client = translate.Client()
    tts_client = texttospeech.TextToSpeechClient()

    with io.open(speech_file, 'rb') as audio_file:
        content = audio_file.read()

    audio = types.RecognitionAudio(content=content)
    config = types.RecognitionConfig(
        #encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        encoding=enums.RecognitionConfig.AudioEncoding.FLAC,
        sample_rate_hertz=AUDIO_CONFIG['rate'],
        language_code='en-US',
        #language_code='de-DE',
        alternative_language_codes=['es-ES','de-DE','pt','el','it'])

    response = client.recognize(config, audio)

    for i, result in enumerate(response.results):
        alternative = result.alternatives[0]
        print('-' * 20)
        print('First alternative of result {}: {}'.format(i, alternative))
        print(u'Transcript: {}'.format(alternative.transcript))

    for result in response.results:
        text = result.alternatives[0].transcript
        target = 'fr'
        translation = translate_client.translate(text,target_language=target)


    try:
        text = translation['translatedText']
    except:
        text = "Je n'arrive pas a traduire le texte"
    print(u'Translation: {}'.format(text))

    #FIXME : translated text may contain &#39; instead of ' - maybe encoding pb - simple replace in first attempt
    text = text.replace("&#39;","'")
    print(u'After decoding: {}'.format(text))

    input_text = texttospeech.types.SynthesisInput(text=text)
    voice = texttospeech.types.VoiceSelectionParams(language_code='fr-FR',ssml_gender=texttospeech.enums.SsmlVoiceGender.FEMALE)
    audio_config = texttospeech.types.AudioConfig(
    audio_encoding=texttospeech.enums.AudioEncoding.LINEAR16)
    response = tts_client.synthesize_speech(input_text, voice, audio_config)

    with open('output.wav', 'wb') as out:
        out.write(response.audio_content)
    print('Audio content written to file "output.mp3"')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        'path', help='File or GCS path for audio file to be recognized')
    args = parser.parse_args()

    transcribe_file(args.path)
