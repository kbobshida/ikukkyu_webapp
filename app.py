from flask import Flask, render_template, request, redirect, url_for, session, jsonify, render_template_string
from flask_session import Session
from datetime import datetime, timedelta
from markdown import markdown
from markupsafe import Markup

app = Flask(__name__)
app.secret_key = 'secret_key'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

@app.template_filter('markdown')
def markdown_filter(text):
    return Markup(markdown(text or "", extensions=["extra", "tables", "fenced_code"]))

@app.route("/", methods=["GET", "POST"])
def form():
    if request.method == "POST":
        responses = {}
        for i in list(range(1, 11)) + list(range(12, 24)) + [27]:
            responses[f'q{i}'] = request.form.get(f'q{i}', '')

        def handle_checkbox(name, other_label, other_input):
            selected = request.form.getlist(name)
            other = request.form.get(other_input, "").strip()
            if other_label in selected and other:
                selected.append(f"（内容：{other}）")
            return "、".join(selected)

        responses["q11"] = handle_checkbox("q11", "③ その他", "q11_other")
        responses["q24"] = handle_checkbox("q24", "⑥ その他", "q24_other")
        responses["q25"] = handle_checkbox("q25", "⑤ その他", "q25_other")
        responses["q26"] = handle_checkbox("q26", "⑧ その他", "q26_other")

        session["responses"] = responses

        with open("templates/prompt_template.txt", "r", encoding="utf-8") as f:
            prompt_template = f.read()
        step1_prompt = render_template_string(prompt_template, responses=responses)
        session["step1_prompt"] = step1_prompt

        session.pop("step2_prompt", None)
        session.pop("carryover_prompt", None)

        return redirect(url_for("result"))

    return render_template("form.html")

@app.route("/result", methods=["GET"])
def result():
    return render_template(
        "result.html",
        prompt=session.get("step1_prompt", ""),
        step2_prompt=session.get("step2_prompt"),
        carryover_prompt=session.get("carryover_prompt"),
        email_prompt=session.get("email_prompt")
    )

@app.route("/followup", methods=["POST"])
def followup():
    selected_plan = request.json.get("selected_plan")
    responses = session.get("responses", {})

    with open("templates/followup_template.txt", "r", encoding="utf-8") as f:
        template = f.read()

    followup_prompt = render_template_string(template, selected_plan=selected_plan, responses=responses)
    session["step2_prompt"] = followup_prompt

    return jsonify({"prompt": followup_prompt})

@app.route("/carryover", methods=["POST"])
def carryover():
    data = request.get_json()
    paid_leave_days = data.get("paid_leave_days", "").strip()
    responses = session.get("responses", {})

    with open("templates/carryover_prompt.txt", "r", encoding="utf-8") as f:
        template = f.read()

    carryover_prompt = render_template_string(template, responses=responses, paid_leave_days=paid_leave_days)
    session["carryover_prompt"] = carryover_prompt

    return jsonify({"prompt": carryover_prompt})

@app.route("/email", methods=["POST"])
def email():
    data = request.get_json()
    target = data.get("email_target", "")
    responses = session.get("responses", {})

    if target == "husband":
        template_path = "templates/email_template_husband.txt"
    elif target == "wife":
        template_path = "templates/email_template_wife.txt"
    else:
        return jsonify({"error": "invalid target"}), 400

    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    email_prompt = render_template_string(template, responses=responses)
    session["email_prompt"] = email_prompt

    return jsonify({"prompt": email_prompt})

@app.route("/calculate", methods=["POST"])
def calculate():
    data = request.get_json()
    due_date_str = data.get("due_date")
    is_multiple = data.get("is_multiple")

    try:
        due_date = datetime.strptime(due_date_str, "%Y-%m-%d")
    except (ValueError, TypeError):
        return jsonify({"error": "無効な日付形式です"}), 400

    pre_days = 97 if is_multiple else 41
    pre_start = due_date - timedelta(days=pre_days)
    pre_end = due_date
    post_start = due_date + timedelta(days=1)
    post_end = due_date + timedelta(weeks=8)

    return jsonify({
        "産前休業開始日": pre_start.strftime("%Y-%m-%d"),
        "産前休業終了日": pre_end.strftime("%Y-%m-%d"),
        "産後休業開始日": post_start.strftime("%Y-%m-%d"),
        "産後休業終了日": post_end.strftime("%Y-%m-%d")
    })

if __name__ == "__main__":
    app.run(debug=True, port=5005)
