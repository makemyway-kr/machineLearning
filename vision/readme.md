컴퓨터비전응용 과제물
20192698 심원준
npm과 node를 설치 후 진행.
officerweb : 마스크 미착용자 고지용 클라이언트 웹(React)으로 npm i를 실행 해 필요한 파일들 다운로드 후 npm start로 웹 서버 시작.
Server : 비전 프로세스에 필요한 서버 코드 폴더.
socketServer: 웹소켓 중계 서버, (node.js)로 마찬가지로 npm i 후 npm start로 시작.
videoClient.py : 비디오 송신용 프로그램. python videoClient.py로 시작.
videoProcess.py : 비디오 처리 및 마스크 착용 여부 분류기(ML서버)
modelLearning.py : 이미지 분류기 학습용 코드
requirements.txt에 들어있는 모듈들을 pip install -r requirements.txt 로 설치.

logs : 학습 과정 로그, tensorboard --logdir=./logs/fit로 tensorboard 실행 후 
브라우저를 통해 localhost:6006에 접속하면 그래프 및 정보 확인 가능.