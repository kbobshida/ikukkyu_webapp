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

        for key in request.form:
            responses[key] = request.form.get(key)

        responses["q11"] = f"{request.form.get('q11_option', '')}：{request.form.get('q11', '')}"
        responses["q12"] = f"{request.form.get('q12_option', '')}：{request.form.get('q12', '')}"
        responses["q15"] = f"{request.form.get('q15_option', '')}：{request.form.get('q15', '')}"

        q18_list = request.form.getlist("q18")
        q18_other = request.form.get("q18_other", "").strip()
        if "⑫ その他" in q18_list and q18_other:
            q18_list.append(f"（内容：{q18_other}）")
        responses["q18"] = "、".join(q18_list)

        q21_list = request.form.getlist("q21")
        q21_other = request.form.get("q21_other", "").strip()
        if "⑤ その他" in q21_list and q21_other:
            q21_list.append(f"（内容：{q21_other}）")
        responses["q21"] = "、".join(q21_list)

        q23_list = request.form.getlist("q23")
        q23_other = request.form.get("q23_other", "").strip()
        if "⑦ その他" in q23_list and q23_other:
            q23_list.append(f"（内容：{q23_other}）")
        responses["q23"] = "、".join(q23_list)

        # セッションに保存して /confirm にリダイレクト
        session["responses"] = responses
        return redirect(url_for("confirm"))

    return render_template("form.html")


@app.route("/confirm", methods=["GET", "POST"])
def confirm():
    responses = session.get("responses", {})
    if request.method == "POST":
        return redirect(url_for("result"))
    return render_template("confirm.html", responses=responses)


@app.route("/result", methods=["GET", "POST"])
def result():
    responses = session.get("responses", {})
    return render_template("result.html", responses=responses)


if __name__ == "__main__":
    app.run(debug=True)
