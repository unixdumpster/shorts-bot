from google.oauth2 import service_account
from google.cloud import speech
from google.cloud import storage

def get_credentials(credentials):
    return service_account.Credentials.from_service_account_file(credentials)

# upload audio file to provided bucket and destination path
def upload_blob(bucket_name, audio_path, destination_path):
    client_file = 'gcs_creds.json'
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
    
# get the google cloud speech to text response object
def long_running_recognize(storage_uri):
    client_file = 'gcs_creds.json'
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

# get the transcript that will be processed in our video creation
def get_transcript(gcs_response, bin_size=0.5):
    # gcs_response is the json response from the speech-to-text api call
    # bin_size is the interval in seconds in which we want to split the response into
    transcript = []
    current_sentence = []
    current_sentence_start = None
    current_sentence_end = None

    for result in gcs_response.results:
        # google responses have alternative transcriptions in which we selected the one the model is most confident in (alternatives[0])
        alternative = result.alternatives[0]
        for word_info in alternative.words:
            # info we have from the json response
            word = word_info.word
            start_time = word_info.start_time
            end_time = word_info.end_time

            # is this the first sentence? if so, need to instantiate the current_sentence start and end times.
            if current_sentence_start is None:
                current_sentence_start = start_time
                current_sentence_end = start_time

            # does current word belong in this bin or next one?
            if current_sentence_end.total_seconds() - current_sentence_start.total_seconds() > bin_size:
                transcript.append(((current_sentence_start.total_seconds(), current_sentence_end.total_seconds()), " ".join(current_sentence)))
                current_sentence = []
                current_sentence_start = start_time

            current_sentence.append(word)
            current_sentence_end = end_time

    # Add the last sentence
    if current_sentence:
        transcript.append(((current_sentence_start.total_seconds(), current_sentence_end.total_seconds()), " ".join(current_sentence)))

    # print(transcript)
    return transcript