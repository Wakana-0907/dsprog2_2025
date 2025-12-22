from flask import Flask, request, render_template_string
app = Flask(__name__)

# HTMLテンプレートそのまま用いて画像マップを設定
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>日本地図選択</title>
</head>
<body>
    <h1>日本地図で地方を選択</h1>
    <img src="日本地図.png" alt="日本地図" usemap="#japan-map">
    <map name="japan-map">
        <area shape="poly" coords="150,50,170,60,190,80,150,90" href="/region?name=北海道">
        <area shape="poly" coords="200,100,220,110,240,130,200,140" href="/region?name=東北">
    </map>
</body>
</html>
"""

@app.route("/")
def index():
    return HTML_TEMPLATE

@app.route("/region")
def show_region():
    region_name = request.args.get("name")
    return f"<h1>{region_name}のデータを取得できます！</h1>"

if __name__ == "__main__":
    app.run(debug=True)
    