# Copyright 2022 David Scripka. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Imports
import pyaudio
import subprocess
import numpy as np
from openwakeword.model import Model
import argparse

# Parse input arguments
parser=argparse.ArgumentParser()
parser.add_argument(
    "--chunk_size",
    help="How much audio (in number of samples) to predict on at once",
    type=int,
    default=1280,
    required=False
)
parser.add_argument(
    "--model_path",
    help="The path of a specific model to load",
    type=str,
    default="",
    required=False
)
parser.add_argument(
    "--inference_framework",
    help="The inference framework to use (either 'onnx' or 'tflite'",
    type=str,
    default='onnx',
    required=False
)

args=parser.parse_args()

# Get microphone stream
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = args.chunk_size
audio = pyaudio.PyAudio()
mic_stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

# Load pre-trained openwakeword models
if args.model_path != "":
    owwModel = Model(wakeword_models=[args.model_path], inference_framework=args.inference_framework)
else:
    wakeword_models = [
        # "./wakeword_models/hey_neo.onnx",
        # "./wakeword_models/type_neo.onnx",
        # "./wakeword_models/bye_neo.onnx",
        # "./wakeword_models/hey_..._neo.onnx",
        # "./wakeword_models/activate_controller.onnx",
        # "./wakeword_models/hey_gram.onnx",
        # "./wakeword_models/goodbye_gram.onnx",
        "./wakeword_models/hi_gram.onnx",
        # "./wakeword_models/goodbye.onnx",
        # "./wakeword_models/shutdown.onnx",
        # "./wakeword_models/good_bye.onnx",
        "./wakeword_models/bye_bye.onnx",
        "./wakeword_models/type_gram.onnx",
    ]
    owwModel = Model(wakeword_models = wakeword_models, inference_framework=args.inference_framework)
    # owwModel = Model(inference_framework=args.inference_framework)

n_models = len(owwModel.models.keys())

isAirControllerOn = False
isKeyboardSTTOn = False
keyboardPrc = None
prev_listen_time = None

# Run capture loop continuosly, checking for wakewords
if __name__ == "__main__":
    # Generate output string header
    print("\n\n")
    print("#"*100)
    print("Listening for wakewords...")
    print("#"*100)
    print("\n"*(n_models*3))

    while True:
        # Get audio
        audio = np.frombuffer(mic_stream.read(CHUNK), dtype=np.int16)

        # Feed to openWakeWord model
        prediction = owwModel.predict(audio)

        # Column titles
        n_spaces = 16
        output_string_header = """
            Model Name         | Score | Wakeword Status
            --------------------------------------
            """

        for mdl in owwModel.prediction_buffer.keys():
            # Add scores in formatted table
            scores = list(owwModel.prediction_buffer[mdl])
            curr_score = format(scores[-1], '.20f').replace("-", "")

            output_string_header += f"""{mdl}{" "*(n_spaces - len(mdl))}   | {curr_score[0:5]} | {"--"+" "*20 if scores[-1] <= 0.5 else "Wakeword Detected!"}
            """
            if scores[-1] >= 0.5:
                print(f"{mdl}: {scores[-1]}")

            # turn on air controller
            if mdl == 'hi_gram' and scores[-1] >= 0.7 and not isAirControllerOn:
                # send 'turn on'
                subprocess.run(['python3', 'command_manager.py', 'on'])
                isAirControllerOn = True
            # turn off mouse controller
            if mdl == 'type_gram' and scores[-1] >= 0.7 and isAirControllerOn:
                subprocess.run(['python3', 'command_manager.py', 'off'])
                # send 'turn off'
                isAirControllerOn = False
            # wake keyboard controller
            if mdl == 'bye_bye' and scores[-1] >= 0.7 and isAirControllerOn:
                # to erase, temp code
                import time
                curr_listen_time = int(time.time())
                if prev_listen_time != None:
                    time_interval = curr_listen_time - prev_listen_time
                else:
                    time_interval = 100
                if time_interval >= 5:                           
                    # send 'turn on'
                    keyboardPrc = subprocess.run(['python3', 'command_manager.py', 'keyboard-listener-on'])
                    print(f'keyboardPrc.check_returncode: {keyboardPrc.check_returncode()}, keyboardPrc: {keyboardPrc}')
                    prev_listen_time = curr_listen_time
