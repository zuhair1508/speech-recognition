import pyaudio
import websockets
import asyncio
import base64
import json
from api_secrets import API_KEY_ASSEMBLYAI
from openai_helper import ask_computer

# Audio Stream Parameters
FRAMES_PER_BUFFER = 3200
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
WAVE_OUTPUT_FILENAME = "output.wav"

# PyAudio to stream the sound from our mic
p = pyaudio.PyAudio()

info = p.get_host_api_info_by_index(0)
numdevices = info.get('deviceCount')

for i in range(0, numdevices):
        if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
            print("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))

index = int(input())

stream = p.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    input_device_index=index,
    frames_per_buffer=FRAMES_PER_BUFFER
)

# Connect to AssemblyAI's Streaming Websocket endpoint
URL = "wss://api.assemblyai.com/v2/realtime/ws?sample_rate=16000"

async def send_receive():
      async with websockets.connect(
            URL,
            ping_timeout=20,
            ping_interval=5,
            extra_headers={'Authorization': API_KEY_ASSEMBLYAI}
      ) as _ws:
            await asyncio.sleep(0.1)
            session_begins = await _ws.recv()
            print(session_begins)
            print("Sending messages")

            async def send():
                while True:
                    try:
                        data = stream.read(FRAMES_PER_BUFFER, exception_on_overflow=False)
                        data = base64.b64encode(data).decode("utf-8")
                        json_data = json.dumps({'audio_data': data})
                        await _ws.send(json_data)
                    except websockets.exceptions.ConnectionClosedError as e:
                        print(e)
                        assert e.code == 4008
                        break
                    except Exception as e:
                        assert False, f"Not a websocket 4008 error. Error: {e}"
                    await asyncio.sleep(0.01)

            async def receive():
                while True:
                    try:
                        result_str = await _ws.recv()
                        result = json.loads(result_str)

                        # 
                        prompt = result['text']
                        if prompt and result['message_type'] == "FinalTranscript":
                            print('Me:', prompt)
                            response = ask_computer(prompt)
                            print("Bot: ", response)
                    except websockets.exceptions.ConnectionClosedError as e:
                        print(e)
                        assert e.code == 4008
                        break
                    except Exception as e:
                        assert False, f"Not a websocket 4008 error. Error: {e}"
                    await asyncio.sleep(0.01)

            send_result, receive_results = await asyncio.gather(send(), receive())

asyncio.run(send_receive())