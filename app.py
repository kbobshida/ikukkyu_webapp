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
        for i in list(range(1, 11)) + list(range(12, 24)) + [27]:
            responses[f'q{i}'] = request.form.get(f'q{i}', '')

        # チェックボックス＋その他（保育園/幼稚園の入園希望時期）
        q11_list = request.form.getlist("q11")
        q11_other = request.form.get("q11_other", "").strip()
        if "③ その他" in q11_list and q11_other:
            q11_list.append(f"（内容：{q11_other}）")
        responses["q11"] = "、".join(q11_list)

        # チェックボックス＋その他（育休取得で重視したいこと）
        q24_list = request.form.getlist("q24")
        q24_other = request.form.get("q24_other", "").strip()
        if "⑥ その他" in q24_list and q24_other:
            q24_list.append(f"（内容：{q24_other}）")
        responses["q24"] = "、".join(q24_list)

        # チェックボックス＋その他（家事代行・ベビーシッター利用意向）
        q25_list = request.form.getlist("q25")
        q25_other = request.form.get("q25_other", "").strip()
        if "⑤ その他" in q25_list and q25_other:
            q25_list.append(f"（内容：{q25_other}）")
        responses["q25"] = "、".join(q25_list)

        # チェックボックス＋その他（5年後のライフキャリア希望）
        q26_list = request.form.getlist("q26")
        q26_other = request.form.get("q26_other", "").strip()
        if "⑥ その他" in q26_list and q26_other:
            q26_list.append(f"（内容：{q26_other}）")
        responses["q26"] = "、".join(q26_list)

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
