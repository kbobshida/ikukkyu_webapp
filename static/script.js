function calculateDates() {
    const dueDate = document.getElementById("due_date").value;
    const isMultiple = document.getElementById("multiple_yes").checked;
  
    if (!dueDate) {
      alert("出産予定日を入力してください");
      return;
    }
  
    fetch("/calculate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ due_date: dueDate, is_multiple: isMultiple })
    })
      .then(response => response.json())
      .then(data => {
        document.getElementById("pre_start").value = data["産前休業開始日"];
        document.getElementById("pre_end").value = data["産前休業終了日"];
        document.getElementById("post_start").value = data["産後休業開始日"];
        document.getElementById("post_end").value = data["産後休業終了日"];
      });
  }
  

function copyToClipboard(id) {
    const textarea = document.getElementById(id);
    textarea.select();
    textarea.setSelectionRange(0, 99999);
    document.execCommand("copy");
    alert("プロンプトをコピーしました！");
}

document.addEventListener("DOMContentLoaded", () => {
    // ステップ2
    const followupForm = document.getElementById("followupForm");
    if (followupForm) {
        followupForm.addEventListener("submit", async (e) => {
            e.preventDefault();
            const selected_plan = document.getElementById("selected_plan").value;
            if (!selected_plan) return alert("プランを選択してください。");

            const response = await fetch("/followup", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ selected_plan })
            });

            const data = await response.json();
            document.getElementById("step2-result").innerHTML = `
                <button type="button" class="btn secondary-btn" onclick="copyToClipboard('promptText2')">このプロンプトをコピー</button>
                <textarea id="promptText2" class="prompt-text" rows="30">${data.prompt}</textarea>`;
        });
    }

    // ステップ3
    const carryoverForm = document.getElementById("carryoverForm");
    if (carryoverForm) {
        carryoverForm.addEventListener("submit", async (e) => {
            e.preventDefault();
            const days = document.getElementById("paid_leave_days").value;
            if (!days) return alert("日数を入力してください。");

            const response = await fetch("/carryover", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ paid_leave_days: days })
            });

            const data = await response.json();
            document.getElementById("step3-result").innerHTML = `
                <button type="button" class="btn secondary-btn" onclick="copyToClipboard('carryoverPrompt')">このプロンプトをコピー</button>
                <textarea id="carryoverPrompt" class="prompt-text" rows="20">${data.prompt}</textarea>`;
        });
    }

    // ステップ4
    const emailForm = document.getElementById("emailForm");
    if (emailForm) {
        emailForm.addEventListener("submit", async (e) => {
            e.preventDefault();
            const target = document.getElementById("email_target").value;
            if (!target) return alert("対象を選択してください。");

            const response = await fetch("/email", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email_target: target })
            });

            const data = await response.json();
            document.getElementById("step4-result").innerHTML = `
                <button type="button" class="btn secondary-btn" onclick="copyToClipboard('emailPrompt')">メールをコピー</button>
                <textarea id="emailPrompt" class="prompt-text" rows="25">${data.prompt}</textarea>`;
        });
    }
});
