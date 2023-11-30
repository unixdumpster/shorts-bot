from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import os
import sys
from dotenv import load_dotenv

def create_audio(title, content):
    load_dotenv()
    session = Session(aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"), aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"))
    polly = session.client("polly")

    try:
        # Request speech synthesis
        content = (f"{title}") + content
        response = polly.synthesize_speech(Engine="neural", Text=content, OutputFormat="mp3",
                                            VoiceId="Joanna")
    except (BotoCoreError, ClientError) as error:
        # The service returned an error, exit gracefully
        print(error)
        sys.exit(-1)

    if "AudioStream" in response:
        # Note: Closing the stream is important because the service throttles on the
        # number of parallel connections. Here we are using contextlib.closing to
        # ensure the close method of the stream object will be called automatically
        # at the end of the with statement's scope.
        with closing(response["AudioStream"]) as stream:
            path = os.path.join(os.getcwd(), 'raw_audios')
            audio_title = title.strip()[0:16] + ".mp3"
            output = os.path.join(path, f"{audio_title}")
            try:
                # Open a file for writing the output as a binary stream
                with open(output, "wb") as file:
                    file.write(stream.read())
                
                return audio_title
            except IOError as error:
                # Could not write to file, exit gracefully
                print(error)
                sys.exit(-1)

    else:
        # The response didn't contain audio data, exit gracefully
        print("Could not stream audio")
        sys.exit(-1)