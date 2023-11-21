from google.oauth2 import service_account
from google.cloud import speech

def get_transcript(audio_url):
    client_file = 'shorts-bot-405804-476067795df1.json'
    credentials = service_account.Credentials.from_service_account_file(client_file)
    client = speech.SpeechClient(credentials=credentials)

    # load the audio file
    client = speech.SpeechClient()

    with open(audio_url, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        sample_rate_hertz=16000,
        language_code="en-US",
        enable_word_time_offsets=True
    )

    operation = client.long_running_recognize(config=config, audio=audio)

    print("Waiting for operation to complete...")
    result = operation.result(timeout=90)

    transcript = []

    for result in result.results:
        alternative = result.alternatives[0]
        print(f"Transcript: {alternative.transcript}")
        print(f"Confidence: {alternative.confidence}")

        for word_info in alternative.words:
            word = word_info.word
            start_time = word_info.start_time
            end_time = word_info.end_time

            print(
                f"Word: {word}, start_time: {start_time.total_seconds()}, end_time: {end_time.total_seconds()}"
            )

            transcript.append(((start_time.total_seconds(), end_time.total_seconds()), word))

    return transcript