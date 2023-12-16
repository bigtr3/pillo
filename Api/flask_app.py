from muse_graph import generate_plot
from flask import Flask, jsonify, send_file
from muse_eye import generate_num
from muse_alphabeta import generate_rate
from muse_eye_graph import generate_eye

app = Flask(__name__)

@app.route('/plot')
def plot():
    # 그래프를 생성하고 이미지로 변환
    img_buf_combined = generate_plot()

    # 이미지를 웹 서버에 전송
    return send_file(img_buf_combined, mimetype='image/png')

@app.route('/get_number')
def get_number():
    number = generate_num()  # 예시로 숫자 42를 반환
    return jsonify({'number': number})

@app.route('/get_eye')
def get_eye():
    eye = generate_eye() 
    return send_file(eye, mimetype='image/png')

@app.route('/get_rate')
def get_rate():
    rate = generate_rate()
    return jsonify({'rate': rate})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
