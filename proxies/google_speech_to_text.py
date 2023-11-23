from google.oauth2 import service_account
from google.cloud import speech
from google.cloud import storage

def get_credentials(credentials):
    return service_account.Credentials.from_service_account_file(credentials)

def upload_blob(bucket_name, audio_path, destination_path):
    """Uploads a file to the bucket."""
    # bucket_name = "your-bucket-name"
    # source_file_name = "local/path/to/file"
    # destination_blob_name = "storage-object-name"

    client_file = 'shorts-bot-405804-476067795df1.json'
    storage_client = storage.Client(credentials=get_credentials(client_file))
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_path)

    blob.upload_from_filename(audio_path)

    print(
        "File {} uploaded to {}.".format(
            audio_path, destination_path
        )
    )
    return f"gs://{bucket_name}/{destination_path}"
    

def long_running_recognize(storage_uri):
    client_file = 'shorts-bot-405804-476067795df1.json'
    client = speech.SpeechClient(credentials=get_credentials(client_file))

    # load the audio file
    client = speech.SpeechClient()

    config = speech.RecognitionConfig(
        sample_rate_hertz=16000,
        language_code="en-US",
        model="latest_long",
        enable_word_time_offsets=True,
        enable_automatic_punctuation=True
    )

    operation = client.long_running_recognize(config=config, audio={"uri": storage_uri})

    print("Waiting for operation to complete...")
    result = operation.result(timeout=90)

    return result

def get_transcript(gcs_response, bin_size=0.5):
    transcript = []
    current_sentence = []
    current_sentence_start = None
    current_sentence_end = None

    for result in gcs_response.results:
        alternative = result.alternatives[0]
        for word_info in alternative.words:
            word = word_info.word
            start_time = word_info.start_time
            end_time = word_info.end_time

            if current_sentence_start is None:
                current_sentence_start = start_time
                current_sentence_end = start_time

            # print(f"start_time - end_time: {current_sentence_end.total_seconds() - current_sentence_start.total_seconds()}")
            if current_sentence_end.total_seconds() - current_sentence_start.total_seconds() > bin_size:
                # If the current word starts a new sentence
                # print(f"current sentence: {current_sentence} start time: {start_time} end time: {end_time}")
                transcript.append(((current_sentence_start.total_seconds(), current_sentence_end.total_seconds()), " ".join(current_sentence)))
                current_sentence = []
                current_sentence_start = start_time

            current_sentence.append(word)
            current_sentence_end = end_time

    # Add the last sentence
    if current_sentence:
        transcript.append(((current_sentence_start.total_seconds(), current_sentence_end.total_seconds()), " ".join(current_sentence)))

    print(transcript)
    return transcript