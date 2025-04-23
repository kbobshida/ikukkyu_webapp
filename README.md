# ikukyu_webapp

# 育休プラン自動提案Webアプリ

このWebアプリは、出産予定日や家族の状況、育休取得の希望など、23の質問に答えることで、あなたに最適な育休取得プランのプロンプト（AIへの指示文）を自動生成します。生成されたプロンプトは、[ChatGPT](https://chat.openai.com/) に貼り付けて利用できます。

---

## 🌱 特徴

- Flaskで構築された軽量なWebアプリ
- 使いやすい入力フォームと確認画面付き
- 回答内容からChatGPTプロンプトを自動作成
- ローカルで動作、OpenAI APIは使用しません（安全）

---

## 🖥️ 使用方法

### 1. クローンして依存関係をインストール

```bash
git clone https://github.com/yourusername/ikukyu_webapplication.git
cd ikukyu_webapplication
pip install -r requirements.txt
