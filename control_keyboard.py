import google.generativeai as genai
import requests
import json
import ast
import speech_recognition as sr
import keyboard
from pydub import AudioSegment
import io
import time
import pyautogui
import pyperclip
import pygame
import os
import re
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
CLOVA_SPEECH_INVOKE_URL = os.getenv('CLOVA_SPEECH_INVOKE_URL')
CLOVA_SPEECH_SECRET_KEY = os.getenv('CLOVA_SPEECH_SECRET_KEY')

FAIL_COMMENT_RESPONSE = ['경우에 따라 다름', '단축키로 불가', '지시문 없음']
PYAUTOGUI_KEYBOARD_KEYS = ['\t', '\n', '\r', ' ', '!', '"', '#', '$', '%', '&', "'", '(',
')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7',
'8', '9', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`',
'a', 'b', 'c', 'd', 'e','f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~',
'accept', 'add', 'alt', 'altleft', 'altright', 'apps', 'backspace',
'browserback', 'browserfavorites', 'browserforward', 'browserhome',
'browserrefresh', 'browsersearch', 'browserstop', 'capslock', 'clear',
'convert', 'ctrl', 'ctrlleft', 'ctrlright', 'decimal', 'del', 'delete',
'divide', 'down', 'end', 'enter', 'esc', 'escape', 'execute', 'f1', 'f10',
'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f2', 'f20',
'f21', 'f22', 'f23', 'f24', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9',
'final', 'fn', 'hanguel', 'hangul', 'hanja', 'help', 'home', 'insert', 'junja',
'kana', 'kanji', 'launchapp1', 'launchapp2', 'launchmail',
'launchmediaselect', 'left', 'modechange', 'multiply', 'nexttrack',
'nonconvert', 'num0', 'num1', 'num2', 'num3', 'num4', 'num5', 'num6',
'num7', 'num8', 'num9', 'numlock', 'pagedown', 'pageup', 'pause', 'pgdn',
'pgup', 'playpause', 'prevtrack', 'print', 'printscreen', 'prntscrn',
'prtsc', 'prtscr', 'return', 'right', 'scrolllock', 'select', 'separator',
'shift', 'shiftleft', 'shiftright', 'sleep', 'space', 'stop', 'subtract', 'tab',
'up', 'volumedown', 'volumemute', 'volumeup', 'win', 'winleft', 'winright', 'yen',
'command', 'option', 'optionleft', 'optionright']

def is_korean(text):
    # 한글 유니코드 범위: 0xAC00-0xD7AF
    return bool(re.search(r'[\uAC00-\uD7AF]', text))

def is_english(text):
    # 영어 알파벳 범위: a-z, A-Z
    return bool(re.search(r'[a-zA-Z]', text))


class GeminiClient:
    # Gemini key
    api_key = GEMINI_API_KEY
    # prompt = "세 개의 역따옴표로 구분된 텍스트가 제공됩니다. 해당 지시문은 윈도우 내의 단축키, 혹은 키보드 입력으로 만들어 낼 수 있는 명령입니다. 지시문을 윈도우OS의 단축키로 알려주고, 다음 리스트(대괄호와 쉼표로 작성된 배열) 형식으로 재작성 하세요.[[,],[,]].  한번에 누르는 키 조합을  묶고, 여러 핫키를 사용한다면 순서를 사용하세요. 해당 지시문을 실행하는 명령어가 2가지 이상의 서로다른 방식으로 동작된다면, 하나만 선택해서 반환하세요. 가이드는 반환하지 마시오. 만약 제공된 텍스트가 없다면 '지시문 없음'을 작성하세요. 윈도우 단축키로 반환할 수 없다면, '단축키로 불가'을 작성하세요. 그리고 만약 윈도우 브라우저에서 항상 같지 않고, 다른 조건에 따라 키보드 키가 달라진다면, '경우에 따라 다름'을 작성하세요. 지시문이 '브라우저의 두번째 탭을 닫아줘' 일때 반환값은 이것입니다. [['ctrl', '2'], ['ctrl', 'w']]. 지시문이 '역삼역 검색해줘' 일때 반환값은 이것입니다. [['ctrl', 'l'], ['ctrl', 't'], ['역삼역'], ['enter']]. 지시문이 '안녕하세요 입력해줘' 일때 반환값은 이것입니다. [['안녕하세요']]."
    prompt = '''
    세 개의 역따옴표로 구분된 텍스트가 제공됩니다. 
    해당 지시문은 윈도우 내의 단축키, 혹은 키보드 입력으로 만들어 낼 수 있는 명령입니다. 
    지시문을 윈도우OS의 단축키로 알려주고, 다음 리스트(대괄호와 쉼표로 작성된 배열) 형식으로 재작성 하세요.[[,],[,]].  
    한번에 누르는 키 조합을 묶고, 여러 핫키를 사용한다면 순서를 사용하세요. 
    해당 지시문을 실행하는 명령어가 2가지 이상의 서로 다른 방식으로 동작된다면, 하나만 선택해서 반환하세요.
    가이드는 반환하지 마시오. 
    만약 제공된 텍스트가 없다면 '지시문 없음'을 작성하세요. 
    윈도우 단축키로 반환할 수 없다면, '단축키로 불가'을 작성하세요.
    지시문에 '검색해줘', '입력해줘'가 없고, 윈도우 단축키로 반환할 수 없다면, '단축키로 불가'를 작성하세요.
    그리고 만약 윈도우 브라우저에서 항상 같지 않고, 다른 조건에 따라 키보드 키가 달라진다면, '경우에 따라 다름'을 작성하세요. 

    지시문이 '브라우저의 두번째 탭을 닫아줘' 일때 반환값은 이것입니다. 
    [['ctrl', '2'], ['ctrl', 'w']]. 
    지시문이 '역삼역 검색해줘' 일때 반환값은 이것입니다. 
    [['ctrl', 'l'], ['ctrl', 't'], ['역삼역'], ['enter']]. 
    지시문이 '안녕하세요 입력해줘' 일때 반환값은 이것입니다. [['안녕하세요']].
    '''

    keyboard_condition = "사용할 수 있는 키보드는 다음 중에서 선택합니다. [\t, \n, \r,  , !, ', #, $, %, &, \", (,), *, +, ,, -, ., /, 0, 1, 2, 3, 4, 5, 6, 7,8, 9, :, ;, <, =, >, ?, @, [, \\, ], ^, _, `,a, b, c, d, e,f, g, h, i, j, k, l, m, n, o,p, q, r, s, t, u, v, w, x, y, z, {, |, }, ~,accept, add, alt, altleft, altright, apps, backspace,browserback, browserfavorites, browserforward, browserhome,browserrefresh, browsersearch, browserstop, capslock, clear,convert, ctrl, ctrlleft, ctrlright, decimal, del, delete,divide, down, end, enter, esc, escape, execute, f1, f10,f11, f12, f13, f14, f15, f16, f17, f18, f19, f2, f20,f21, f22, f23, f24, f3, f4, f5, f6, f7, f8, f9,final, fn, hanguel, hangul, hanja, help, home, insert, junja,kana, kanji, launchapp1, launchapp2, launchmail,launchmediaselect, left, modechange, multiply, nexttrack,nonconvert, num0, num1, num2, num3, num4, num5, num6,num7, num8, num9, numlock, pagedown, pageup, pause, pgdn,pgup, playpause, prevtrack, print, printscreen, prntscrn,prtsc, prtscr, return, right, scrolllock, select, separator,shift, shiftleft, shiftright, sleep, space, stop, subtract, tab,up, volumedown, volumemute, volumeup, win, winleft, winright, yen,command, option, optionleft, optionright]"

    genai.configure(api_key=api_key)

    def req_generate(self, order):
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        generation_config = genai.GenerationConfig(temperature=0)       # temperature 0으로 셋팅
        message = self.prompt + self.keyboard_condition+ "```" + order + "```"
        response = model.generate_content(message, generation_config=generation_config)
        return response.text


class ClovaSpeechClient:
    # Clova Speech invoke URL
    invoke_url = CLOVA_SPEECH_INVOKE_URL
    # Clova Speech secret key
    secret = CLOVA_SPEECH_SECRET_KEY

    def req_upload(self, file, completion, callback=None, userdata=None, forbiddens=None, boostings=None,
                   wordAlignment=True, fullText=True):
        request_body = {
            'language': 'ko-KR',
            'completion': completion,
            'callback': callback,
            'userdata': userdata,
            'wordAlignment': wordAlignment,
            'fullText': fullText,
            'forbiddens': forbiddens,
            'boostings': boostings,
        }
        headers = {
            'Accept': 'application/json;UTF-8',
            'X-CLOVASPEECH-API-KEY': self.secret
        }
        print(json.dumps(request_body, ensure_ascii=False).encode('UTF-8'))
        files = {
            'media': open(file, 'rb'),
            'params': (None, json.dumps(request_body, ensure_ascii=False).encode('UTF-8'), 'application/json')
        }
        response = requests.post(headers=headers, url=self.invoke_url + '/recognizer/upload', files=files)
        return response


def extract_and_convert_2d_array(string):
    # 앞뒤 불필요한 말 제거하고, [[ ]] 안의 내용만 추출
    # [[와 ]]의 위치를 찾아서 해당 부분을 추출

    start = string.find('[[')
    end = string.find(']]') + 2
    
    if start == -1 or end == 1:
        return False
    
    array_string = string[start:end]
    return array_string


class EffectSoundClient:
    pygame.mixer.init()
    # 효과음 파일 로드
    start_sound = pygame.mixer.Sound('./sound/start.wav')
    end_sound = pygame.mixer.Sound('./sound/end.wav')
    success_sound = pygame.mixer.Sound('./sound/success.mp3')
    fail_sound = pygame.mixer.Sound('./sound/fail.wav')
    def play_start_sound(self):
        self.start_sound.play()
        # time.sleep(2)
    def play_end_sound(self):
        self.end_sound.play()
        # time.sleep(2)
    def play_success_sound(self):
        self.success_sound.play()
        # time.sleep(2)
        # Pygame 믹서 종료
        pygame.mixer.quit()
    def play_fail_sound(self):
        self.fail_sound.play()
        # time.sleep(1.9)
        # Pygame 믹서 종료
        pygame.mixer.quit()

if __name__ == '__main__':
    # FFmpeg 경로 설정
    ffmpeg_path = r"C:\ffmpeg\bin\ffmpeg.exe"

    # 환경 변수에 FFmpeg 경로 추가
    os.environ["PATH"] += os.pathsep + os.path.dirname(ffmpeg_path)

    recognizer = sr.Recognizer()
    

    # 마이크 인식 시작
    # 마이크 초기화 및 배경 소음 조정
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        print("마이크 준비 완료")

    with sr.Microphone() as source:
        # q가 눌리면 음성 녹음 시작 ---> 시동어 인식하면으로 수정하기
        # 마이크 시작 효과음
        EffectSoundClient().play_start_sound()
        print("# =================")
        print("Listening...")

        audio_data = recognizer.listen(source, phrase_time_limit=3)
        audio_bytes = audio_data.get_wav_data()
        # Convert the WAV audio data to an AudioSegment
        audio_segment = AudioSegment.from_wav(io.BytesIO(audio_bytes))

        # Save the AudioSegment as an MP3 file
        audio_segment.export("./recorded_audio.mp3", format="mp3")
        print("Audio has been saved to recorded_audio.mp3")
        print("# =================")
        # 마이크 종료 효과음
        EffectSoundClient().play_end_sound()
        
        try:
            res = ClovaSpeechClient().req_upload(file='./recorded_audio.mp3', completion='sync')   
                
            json_res = json.loads(res.text)
            print(f"json 결과: {json_res}")

            is_command_input = False
            stt_res = json_res["text"]
            print(f"stt 인식된 텍스트: {stt_res}")

            if '입력해' in stt_res:
                is_command_input = True

            # text를 Gemini api 입력으로 넣고 호출
            commands = GeminiClient().req_generate(stt_res).strip()
            print(f"Gemini 결과: {commands}")

            array_format_commands = extract_and_convert_2d_array(commands)
            print(array_format_commands)

            if array_format_commands != False:
                # 명령이 "입력해줘"인 경우
                if is_command_input:
                    input_word = "" # 입력할 텍스트

                    '''
                        array_format_commands: 2d list
                        command: 1d list
                    '''
                    for command in ast.literal_eval(array_format_commands):
                        print("###", command)

                        # 입력해줘 명령어면 텍스트만 입력해야함. 따라서 그 외 ctrl 명령은 무시
                        if command[0] == 'ctrl' or '입력해' in command[0]:
                            continue
                        print(input_word)

                        for comm in command:
                            if "입력해" in comm:
                                continue
                            
                            if comm not in PYAUTOGUI_KEYBOARD_KEYS:
                                # 키가 아닌 텍스트면 input_word로 추가
                                input_word += comm
                            else:
                                pyautogui.hotkey(comm)

                    print(f"최종 input word: {input_word}")

                    if input_word:
                        if is_korean(input_word):
                            # 한국어면 copy후 붙여넣기 (pyautogui가 한국어 지원 안하기 때문)
                            pyperclip.copy(input_word)
                            pyautogui.hotkey("ctrl", "v")
                        elif is_english(input_word):
                            # 영어면 바로 write
                            pyautogui.write(input_word)
                    
                # 그 외  
                else:
                    for command in ast.literal_eval(array_format_commands):
                        if command[0] in FAIL_COMMENT_RESPONSE:
                            raise Exception("FAIL_COMMENT_RESPONSE")
                        
                        if command[0] not in PYAUTOGUI_KEYBOARD_KEYS:
                            pyperclip.copy(command[0])
                            pyautogui.hotkey("ctrl", "v")

                        else:
                            # pyautogui로 키보드 조작
                            pyautogui.hotkey(*command)

                EffectSoundClient().play_success_sound()
            else:
                raise Exception("FAIL_2D_ARRAY")

                
        except Exception as e:
            print("EXCEPTION")
            EffectSoundClient().play_end_sound()
