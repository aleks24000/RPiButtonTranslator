#!/usr/bin/env python

# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Google Cloud Speech API sample application using the REST API for batch
processing.

Example usage:
    python transcribe.py resources/audio.raw
    python transcribe.py gs://cloud-samples-tests/speech/brooklyn.flac
"""

import argparse
import io


# [START speech_transcribe_sync]
def transcribe_file(speech_file):
    """Transcribe the given audio file."""
    from google.cloud import speech_v1p1beta1 as speech
    from google.cloud.speech_v1p1beta1 import enums
    from google.cloud.speech_v1p1beta1 import types
    from google.cloud import translate as translate
    from google.cloud import texttospeech
    import os

    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "gspeech.json"


    client = speech.SpeechClient()
    translate_client = translate.Client()
    tts_client = texttospeech.TextToSpeechClient()

    # [START speech_python_migration_sync_request]
    # [START speech_python_migration_config]
    with io.open(speech_file, 'rb') as audio_file:
        content = audio_file.read()

    audio = types.RecognitionAudio(content=content)
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.FLAC,
        sample_rate_hertz=16000,
        language_code='en-US',
        alternative_language_codes=['es-ES','de-DE','pt','el','it'])
    # [END speech_python_migration_config]

    # [START speech_python_migration_sync_response]
    response = client.recognize(config, audio)
    # [END speech_python_migration_sync_request]
    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    #for result in response.results:
        # The first alternative is the most likely one for this portion.
        #print(u'Transcript: {}'.format(result.alternatives[0].transcript))
    
    for i, result in enumerate(response.results):
        alternative = result.alternatives[0]
        print('-' * 20)
        print('First alternative of result {}: {}'.format(i, alternative))
        print(u'Transcript: {}'.format(alternative.transcript))
   
    print('Translation')
    for result in response.results:
        text = result.alternatives[0].transcript
        target = 'fr'
        translation = translate_client.translate(text,target_language=target)

    print(u'Translation: {}'.format(translation['translatedText']))
    text = translation['translatedText']
    input_text = texttospeech.types.SynthesisInput(text=text)
    voice = texttospeech.types.VoiceSelectionParams(language_code='fr-FR',ssml_gender=texttospeech.enums.SsmlVoiceGender.FEMALE)
    audio_config = texttospeech.types.AudioConfig(
    audio_encoding=texttospeech.enums.AudioEncoding.LINEAR16)
    response = tts_client.synthesize_speech(input_text, voice, audio_config)
    # The response's audio_content is binary.
    with open('output.wav', 'wb') as out:
        out.write(response.audio_content)
    print('Audio content written to file "output.mp3"')

    # [END speech_python_migration_sync_response]
# [END speech_transcribe_sync]


# [START speech_transcribe_sync_gcs]
def transcribe_gcs(gcs_uri):
    """Transcribes the audio file specified by the gcs_uri."""
    from google.cloud import speech
    from google.cloud.speech import enums
    from google.cloud.speech import types
    client = speech.SpeechClient()

    # [START speech_python_migration_config_gcs]
    audio = types.RecognitionAudio(uri=gcs_uri)
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.FLAC,
        sample_rate_hertz=16000,
        language_code='en-US')
    # [END speech_python_migration_config_gcs]

    response = client.recognize(config, audio)
    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    for result in response.results:
        # The first alternative is the most likely one for this portion.
        print(u'Transcript: {}'.format(result.alternatives[0].transcript))
# [END speech_transcribe_sync_gcs]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        'path', help='File or GCS path for audio file to be recognized')
    args = parser.parse_args()
    if args.path.startswith('gs://'):
        transcribe_gcs(args.path)
    else:
        transcribe_file(args.path)
