from flask import Flask
import pandas as pd

app = Flask(__name__)

# 테스트용 데이터
data = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

@app.route('/')
def display_table():
    df = pd.DataFrame(data, columns=['A', 'B', 'C'], index=['X', 'Y', 'Z'])
    return df.to_html()

if __name__ == '__main__':
    app.run(debug=True)
