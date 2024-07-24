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
pip install -r requirements.txt
```
### Running
상시 wake word를 듣는 프로그램을 실행시킵니다.
```sh
python open_wake_word.py
```
>*만약 라즈베리파이 보드 환경에서 사용중이라면, socket 통신을 위한 server, client 프로그램을 실행시킵니다.*
>```sh
># 보드 환경에서 server 실행
>python server.py
># pc 환경에서 client 실행
>python client.py
>```

이후 원하는 동작을 실행시키는 wake word 를 말합니다.
```sh
# 제어 프로그램 실행 (마우스 제어 프로그램)
"hi gram"

# 키보드 제어 프로그램 실행
"type gram"

# 제어 프로그램 종료
"bye bye"
```
## Use Example


이 프로젝트는 음성 명령과 손 동작을 인식하여 다양한 작업을 수행할 수 있도록 돕습니다. 아래는 사용 방법의 예제입니다.

1. **시작 준비**
   - "hi gram"이라고 말하여 시스템을 활성화합니다.

2. **손 동작 인식**
   - 캠을 향해 손을 움직이며 마우스를 조작합니다.
   - [손 동작 예시 이미지 삽입 예정]

3. **텍스트 입력 준비**
   - "type gram"이라고 말하여 텍스트 입력 모드를 활성화합니다.

4. **브라우저 탭 전환**
   - "브라우저 2번째 탭으로 가줘"라고 말하여 브라우저의 두 번째 탭으로 이동합니다.

5. **검색 준비**
   - 다시 "type gram"이라고 말하여 텍스트 입력 모드를 준비합니다.

6. **검색 수행**
   - "역삼역 맛집 검색해"라고 말하여 검색을 수행합니다.

7. **마우스 클릭**
   - 손을 움직이며 마우스를 조작하여 버튼을 클릭합니다.
   - [마우스 클릭 예시 이미지 삽입 예정]

이러한 과정을 통해 음성과 손 동작을 활용하여 직관적으로 시스템을 제어할 수 있습니다.

## Developer

  <table>
  <tr>
  <td style="width: 50px;"><img src="https://github.com/user-attachments/assets/88da96ce-a1ff-4d1e-9640-55dbc64dd6f9" alt="Alt text" width="80px" /> </td>
  <td style="width: 50px;"><img src="https://github.com/user-attachments/assets/d3b53f06-b0eb-4860-8e28-e9e01a66348b" alt="Alt text" width="80px" /> </td>
  <td style="width: 50px;"><img src="https://github.com/user-attachments/assets/f5e72b8f-eada-4f29-a1b4-dbfd659dc513" alt="Alt text" width="80px" /> </td>
  <td style="width: 50px;"><img src="https://github.com/user-attachments/assets/c6a96288-bc5b-450f-a82b-4621a99d3f04" alt="Alt text" width="80px" /> </td>
  </tr>
  <tr>
  <td  style="width: 70px;">
      <a href="https://github.com/shaqok">
      <sub><img src="https://img.shields.io/badge/김대연-ffffff?style=for-the-badge&logo=github&logoColor=black"></sub></a>
   </td><td  style="width: 70px;">
      <a href="https://github.com/seastark87">
      <sub><img src="https://img.shields.io/badge/김해성-ffffff?style=for-the-badge&logo=github&logoColor=black"></sub></a>
   </td><td  style="width: 70px;">
      <a href="https://github.com/hexaspace">
      <sub><img src="https://img.shields.io/badge/이도연-ffffff?style=for-the-badge&logo=github&logoColor=black"></sub></a>
   </td>
  <td  style="width: 70px;">
      <a href="https://github.com/hangyeolhong">
      <sub><img src="https://img.shields.io/badge/홍한결-ffffff?style=for-the-badge&logo=github&logoColor=black"></sub></a>
   </td>
  </tr>
  </table>
<!-- Markdown link & img dfn's -->

[python]: https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white
[flask]: https://img.shields.io/badge/flask-000000?style=flat-square&logo=flask&logoColor=white
[naver]: https://img.shields.io/badge/CLOVA-03C75A?style=flat-square&logo=naver&logoColor=white
[googlegemini]: https://img.shields.io/badge/GEMINI-8E75B2?style=flat-square&logo=googlegemini&logoColor=white
[socketdotio]: https://img.shields.io/badge/Socket-010101?style=socketdotio-square&logo=socketdotio&logoColor=white

