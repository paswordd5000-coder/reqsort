from flask import Flask, render_template, request

app = Flask(__name__)


def analyze_requirements(text: str):
    lines = [line.strip(' -・\t') for line in text.splitlines() if line.strip()]
    functional, nonfunctional, questions = [], [], []
    nf_words = ('性能', '秒', '可用性', 'セキュリティ', '同時', 'バックアップ', '稼働', 'レスポンス')
    vague_words = ('簡単', '使いやすい', '適切', '高速', 'なるべく', '十分')
    for line in lines:
        if any(word in line for word in nf_words):
            nonfunctional.append(line)
        else:
            functional.append(line)
        if any(word in line for word in vague_words):
            questions.append(f'「{line}」の判定基準を数値または具体例で明確にする必要がある。')
    if not lines:
        questions.append('要望を一行に一件ずつ入力する必要がある。')
    return functional, nonfunctional, questions


@app.route('/', methods=['GET', 'POST'])
def index():
    text = ''
    result = None
    if request.method == 'POST':
        text = request.form.get('requirements', '')
        result = analyze_requirements(text)
    return render_template('index.html', text=text, result=result)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
