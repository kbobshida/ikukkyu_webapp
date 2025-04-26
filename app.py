from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session

app = Flask(__name__)
app.secret_key = 'secret_key'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

@app.route("/", methods=["GET", "POST"])
def form():
    if request.method == "POST":
        responses = {}

        # 単一回答（テキスト・日付・ラジオボタン）
        for i in range(1, 9):
            responses[f'q{i}'] = request.form.get(f'q{i}', '')
        for i in range(10, 22):
            responses[f'q{i}'] = request.form.get(f'q{i}', '')
        responses['q25'] = request.form.get('q25', '')

        # チェックボックス＋その他（保育園入園希望時期）
        q9_list = request.form.getlist("q9")
        q9_other = request.form.get("q9_other", "").strip()
        if "⑦ その他" in q9_list and q9_other:
            q9_list.append(f"（内容：{q9_other}）")
        responses["q9"] = "、".join(q9_list)

        # チェックボックス＋その他（育休取得で重視したいこと）
        q22_list = request.form.getlist("q22")
        q22_other = request.form.get("q22_other", "").strip()
        if "⑫ その他" in q22_list and q22_other:
            q22_list.append(f"（内容：{q22_other}）")
        responses["q22"] = "、".join(q22_list)

        # チェックボックス＋その他（家事代行・ベビーシッター利用意向）
        q23_list = request.form.getlist("q23")
        q23_other = request.form.get("q23_other", "").strip()
        if "⑤ その他" in q23_list and q23_other:
            q23_list.append(f"（内容：{q23_other}）")
        responses["q23"] = "、".join(q23_list)

        # チェックボックス＋その他（5年後のライフキャリア希望）
        q24_list = request.form.getlist("q24")
        q24_other = request.form.get("q24_other", "").strip()
        if "⑧ その他" in q24_list and q24_other:
            q24_list.append(f"（内容：{q24_other}）")
        responses["q24"] = "、".join(q24_list)

        # セッション保存してリダイレクト
        session["responses"] = responses
        return redirect(url_for("result"))

    return render_template("form.html")

@app.route("/result", methods=["GET"])
def result():
    responses = session.get("responses", {})
    return render_template("result.html", responses=responses)

if __name__ == "__main__":
    app.run(debug=True)
