# 내 MAM (reMote Air Manager) 대로
> 손 제스처와 음성으로 디스플레이를 제어

<!-- [![NPM Version][npm-image]][npm-url] -->
![Python][python]
![flask][flask]
![GEMINI][googlegemini]
![CLOVA][naver]
![Socket][socketdotio]

PC, 노트북 모니터, 키오스크 등 여러 디스플레이를 멀리 떨어진 곳에서도 손과 음성으로 디스플레이를 제어합니다.

모션 인식 및 음성 인식 기술 활용을 통한 마우스, 키보드 조작 구현

![](../header.png)


## Getting Started
본 프로젝트는 2가지 방법의 환경이 존재합니다.
1. 라즈베리 파이와 노트북 연동
2. 노트북에서만 동작   

라즈베리 파이 코드는 실습 환경을 구축하기 어렵기 때문에, 모든 동작은 노트북에서 실행하는 것으로 가정합니다. 라즈베리 파이 세팅방법은 "보드 코드" 폴더 내 README를 참고해주세요.
### Prerequisites

control_keyboard.py에서 필요한 FFmpeg 프로그램은 별도로 설치해야합니다.
FFmpeg는 영상과 음성을 변환 및 편집할 수 있는 커맨드라인 프로그램입니다.

OS X & 리눅스:

```sh
sudo apt install ffmpeg
```

윈도우:

1. https://ffmpeg.org/download.html 에서 Essentials 의 zip을 다운로드
2. 3과 4중 원하는 방식으로 환경변수 추가
3. 설치한 폴더의 \ffmpeg\bin를 윈도우 환경변수에 추가
4. 아래과 같은 코드를 control_keyboard.py의 main 함수 처음에 추가
```sh
# FFmpeg 경로 설정
ffmpeg_path = r"C:\ffmpeg\bin\ffmpeg.exe"

# 환경 변수에 FFmpeg 경로 추가
os.environ["PATH"] += os.pathsep + os.path.dirname(ffmpeg_path)
```
### Installing

pip 명령어를 사용하여 필요 패키지를 다운로드

```
pip install ~~~
```
### Running
상시 wake word를 듣는 프로그램을 실행시킵니다.
```
python open_wake_word.py
```


## Break down into end to end tests

Explain what these tests test and why

```
Give an example
```



<!-- Markdown link & img dfn's -->
[npm-image]: https://img.shields.io/npm/v/datadog-metrics.svg?style=flat-square
[npm-url]: https://npmjs.org/package/datadog-metrics
[npm-downloads]: https://img.shields.io/npm/dm/datadog-metrics.svg?style=flat-square
[travis-image]: https://img.shields.io/travis/dbader/node-datadog-metrics/master.svg?style=flat-square
[travis-url]: https://travis-ci.org/dbader/node-datadog-metrics
[wiki]: https://github.com/yourname/yourproject/wiki
[python]: https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white
[flask]: https://img.shields.io/badge/flask-000000?style=flat-square&logo=flask&logoColor=white
[naver]: https://img.shields.io/badge/CLOVA-03C75A?style=flat-square&logo=naver&logoColor=white
[googlegemini]: https://img.shields.io/badge/GEMINI-8E75B2?style=flat-square&logo=googlegemini&logoColor=white
[socketdotio]: https://img.shields.io/badge/Socket-010101?style=socketdotio-square&logo=socketdotio&logoColor=white
[flask]: https://img.shields.io/badge/flask-000000?style=flat-square&logo=flask&logoColor=white

[flask]: https://img.shields.io/badge/flask-000000?style=flat-square&logo=flask&logoColor=white
[flask]: https://img.shields.io/badge/flask-000000?style=flat-square&logo=flask&logoColor=white
[flask]: https://img.shields.io/badge/flask-000000?style=flat-square&logo=flask&logoColor=white
[flask]: https://img.shields.io/badge/flask-000000?style=flat-square&logo=flask&logoColor=white
[flask]: https://img.shields.io/badge/flask-000000?style=flat-square&logo=flask&logoColor=white
