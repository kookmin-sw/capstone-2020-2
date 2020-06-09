# Getting Started
<br/>

### 1. Installations for Face Analyze
<hr/>

- src/analyze/face 폴더로 이동 후 아래의 python 명령어 입력 <br/>
&nbsp;&nbsp;&nbsp;&nbsp; $ pip install pillow <br/>
&nbsp;&nbsp;&nbsp;&nbsp; - face recognition 사용 위한 설정 <br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; $ pip install opencv-python <br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; $ pip install opencv-contrib-python <br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; $ pip install cmake <br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; $ pip install dlib <br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; $ pip install face_recognition <br/>
&nbsp;&nbsp;&nbsp;&nbsp; $ pip install requests <br/>
<br/>

### 2. Installations for EEG analyze
<hr/>

- src/analyze/eeg 폴더로 이동 후, 아래 python 명령어들 입력  <br/>
- "환경설정 완료" 출력이 되면 끝! 다음 스크립트로 쭉쭉 넘어가기 <br/>
- 에러가 나면 아래 명령어로 라이브러리 설치 (anaconda가 아니면 conda를 pip로 대체) <br/><br/>
&nbsp;&nbsp;&nbsp;&nbsp; $ python CustomDatasetClass.py //또는 Models.py <br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; $ conda install pytorch (pip install torch) <br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; $ conda install -c pytorch torchvision (pip install torchvision) <br/>
&nbsp;&nbsp;&nbsp;&nbsp; $ python preprocessModule.py //또는 sensorModule.py <br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; $ pip install brainflow <br/>
&nbsp;&nbsp;&nbsp;&nbsp; $ python transformModule.py <br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; $ conda install scipy <br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; - pyeeg 설치 <br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; $ git clone https://github.com/forrestbao/pyeeg.git <br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; $ cd pyeeg <br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; $ python setup.py install //home 디렉토리에 설치하고 싶으면 끝에 —user 옵션 추가 <br/>
&nbsp;&nbsp;&nbsp;&nbsp; $ python eegAnalyzeModule.py <br/>
&nbsp;&nbsp;&nbsp;&nbsp; $ python plotModule.py <br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; $ conda install matplotlib <br/>
&nbsp;&nbsp;&nbsp;&nbsp; $ python record_signal.py n //마지막 n 까지 입력해야함. <br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; $ pip install keyboard <br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; - 끝에 n대신 y옵션을 주면 실제 연결된 센서로부터 받아오는 신호를 저장 <br/><br/>
<br/>

### 3. Installations for Server&DB (Django, MySQL)
<hr/>

- django 설치 <br/>
&nbsp;&nbsp;&nbsp;&nbsp; $ pip install django <br/><br/>
- DB 설정 <br/>
&nbsp;&nbsp;&nbsp;&nbsp; - src/back-end/FBI/mysql.cnf 파일 수정 <br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  [client] <br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  database = 'db_name' <br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  host = localhost <br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  user = root <br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  password = 'mypassword' <br/>
&nbsp;&nbsp;&nbsp;&nbsp; - src/back-end/FBI/settings.py에 INSTALLED_APP 안의 'api’ 주석 처리 <br/>
&nbsp;&nbsp;&nbsp;&nbsp; - src/back-end/FBI 에서 <br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; $ ./manage.py migrate <br/>
&nbsp;&nbsp;&nbsp;&nbsp; - src/back-end/FBI/settings.py에 INSTALLED_APP 안의 'api’ 주석 처리 해제 <br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; $ ./manage.py makemigrations <br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; $ ./manage.py migrate <br/>
<br/>

### 4. Installations for Client (React)
<hr/>

- src/front-end 폴더 이동 후 <br/>
&nbsp;&nbsp;&nbsp;&nbsp; $npm install <br/>
<br/>
