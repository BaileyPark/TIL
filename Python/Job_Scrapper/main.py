from flask import Flask, render_template, request, redirect, send_file
from scrapper import get_jobs
from export import save_to_file

app = Flask("SuperScrapper")

db = {} # fakeDB = dictionary

@app.route("/") # -> index.html
def home(): # 바로 밑에 있어야 함, 간격 금지, 함수 이름 아무거나 상관없음
  return render_template("index.html") ## templates/index.html 렌더링 (templates 디렉토리명이 바뀌면 안됨)

@app.route("/report") # -> index html or report.html
def report():
  word = request.args.get('word') ## request.args 내부 key/value 형태, 고로 request.args.['word'] 도 가능
  word = word.strip() # 공백제거
  if word:
    word = word.lower() # 소문자화
    existingJobs = db.get(word) # fakeDB내 word 있으면 existingJobs에 넣기
    if existingJobs: 
      jobs = existingJobs
    else:
      jobs = get_jobs(word) # scrapper.py의 get_jobs 메소드
      db[word] = jobs # get_jobs 메소드값, fakeDB에 삽입
  else:
     return redirect("/") # word 없으면, root(index.html)로 리다이렉트
  # return render_template("unittest.html", jobs = jobs) # 유닛테스트용
  return render_template("report.html", searchingBy=word, resultNumber=len(jobs), jobs = jobs) # templates/report.html 렌더링 (searchingBy, resultNumber, jobs 인자값 전송)

@app.route('/export')
def export():
  try:
    word = request.args.get("word")
    if not word: # word가 없으면
      raise # 나가리다, Exception()은 노출할 게 없어 삭제
    # word = word.lower() # 소문자화 (이미 /report에서 소문자화를 했기에 주석)
    jobs = db.get(word) # fakeDB에서 추출
    if not jobs: # 추출데이터가 없으면
      raise # 나가리다
    save_to_file(jobs, word) # export.py의 save_to_file 메소드 실행
    return send_file(f"{word}.csv") # word.csv 다운로드
  except:
    return redirect('/') #나가리면, root(index.html)로 리다이렉트

app.run(host="0.0.0.0") # repl.co 내부 실행