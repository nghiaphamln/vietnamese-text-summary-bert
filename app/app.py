from flask import Flask, request, jsonify
import torch
from models.model_builder import ExtSummarizer
from newspaper import Article
from ext_sum import summarize

app = Flask(__name__)


def load_model(model_type):
    checkpoint = torch.load(f'checkpoints/{model_type}_ext.pt', map_location='cpu')
    _model = ExtSummarizer(device="cpu", checkpoint=checkpoint, bert_type=model_type)
    return _model


def crawl_url(_url):
    article = Article(_url)
    article.download()
    article.parse()
    return article.text


# Load model
model = load_model('mobilebert')


@app.route('/')
def welcome():
    return jsonify({
        'message': 'Chào mừng bạn đến với API tóm tắc văn bản Tiếng Việt'
    })


@app.route('/text-summary', methods=['POST'])
def text_summary_api():
    data = request.get_json()
    try:
        # chỗ này là lấy dữ liệu nè, nếu dữ liệu bị thiếu sẽ trả về lỗi
        data_type = data['type']
        text = data['text']
        length = data['length']

        # chỗ này là độ dài văn bản tóm tắt mong muốn nè
        if length == 'short':
            max_length = 3
        elif length == 'long':
            max_length = 5
        else:
            resp = jsonify({
                'message': 'Bad Request - Invalid data'
            })
            resp.status_code = 400
            return resp

        # chỗ này là xử lí nếu muốn truyền vào một url nè
        if data_type == 'url':
            try:
                text = crawl_url(text)
                input_fp = "raw_data/input.txt"
                with open(input_fp, 'w', encoding="utf-8") as file:
                    file.write(text)
                result_fp = 'results/summary.txt'
                summary = summarize(input_fp, result_fp, model, max_length=max_length)
                return jsonify({
                    'text': summary
                })
            except Exception as ex:
                print(ex)
                resp = jsonify({
                    'message': 'Bad Request - Invalid url'
                })
                resp.status_code = 400
                return resp
        # chỗ này xử lí nếu muốn truyền vào một văn bản bình thường nè
        elif data_type == 'raw_data':
            input_fp = "raw_data/input.txt"
            with open(input_fp, 'w', encoding="utf-8") as file:
                file.write(text)
            result_fp = 'results/summary.txt'
            summary = summarize(input_fp, result_fp, model, max_length=max_length)
            return jsonify({
                'text': summary
            })
        else:
            resp = jsonify({
                'message': 'Bad Request - Invalid data type'
            })
            resp.status_code = 400
            return resp

    # chỗ này là chỗ trả về nếu dữ liệu không hợp lệ nè
    except Exception as ex:
        print(ex)
        resp = jsonify({
            'message': 'Bad Request - Invalid data'
        })
        resp.status_code = 400
        return resp


if __name__ == '__main__':
    app.run()
