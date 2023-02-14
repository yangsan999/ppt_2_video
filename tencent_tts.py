import json
import os
import asyncio
import aiohttp
import argparse

# pip install tencentcloud-sdk-python
from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.tts.v20190823 import models, tts_client

# Read configuration from command-line parsing
parser = argparse.ArgumentParser(
    description='PPT to Video need to use TencentCloud TTS SECRET_ID and SECRET_KEY.')
parser.add_argument('--id', help='Enter your SecretId')
parser.add_argument('--key', help='Enter your SECRET_KEY')
args = parser.parse_args()
SECRET_ID = args.id
SECRET_KEY = args.key

# The maximum number of concurrent HTTP requests
MAX_CONCURRENT_REQUESTS = 20

# The semaphore to limit the number of concurrent HTTP requests
semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)


async def create_tts_task(note, session_id, session):
    # Acquire the semaphore
    async with semaphore:

        # Create a Tencent Cloud credential object
        cred = credential.Credential(SECRET_ID, SECRET_KEY)

        # Create a TTS client
        client = tts_client.TtsClient(cred, "ap-guangzhou")

        # Set the request parameters
        req = models.CreateTtsTaskRequest()
        params = {
            "Text": note,
            "SessionId": str(session_id),
            "ModelType": 1,
            "Speed": 0,
            "SampleRate": 16000,
            "Codec": "mp3",
            "Volume": 0,
            "VoiceType": 101024,
        }
        req.from_json_string(json.dumps(params))

        # Call the TTS service
        try:
            resp = client.CreateTtsTask(req)
            print(str(session_id)+" TTS Task is success")
            task_id = resp.Data.TaskId
        except TencentCloudSDKException as err:
            print(err)
            return None

        # Wait for the task to complete
        while True:
            task_req = models.CreateTtsTaskResponse()
            task_req.TaskId = task_id
            task_resp = client.DescribeTtsTaskStatus(task_req)
            if task_resp.Data.StatusStr == "success":
                print(str(task_id)+" Describe TTS task status is success")
                return task_resp.Data.ResultUrl
            elif task_resp.Data.StatusStr == "failed":
                print("TTS task failed: {}".format(task_resp.ErrorMessage))
                return None
            # Wait for 1 second before checking the task status again
            await asyncio.sleep(1)


async def get_tts_result(task_id, index, session, temp_path):
    # Acquire the semaphore
    async with semaphore:
        async with aiohttp.ClientSession() as session:
            async with session.get(task_id) as resp:
                audio_bytes = await resp.read()

    # Save the bytes to a file
    with open(os.path.join(temp_path, 'slide_{}.mp3'.format(index)), 'wb') as f:
        f.write(audio_bytes)
        print('slide_{}.mp3'.format(index) + " write is success")
