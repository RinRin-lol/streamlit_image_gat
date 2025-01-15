import streamlit as st
import openai
import os

# OpenAI APIキーの設定
openai.api_key = "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"
openai migrate

# スタイルのカスタマイズ
st.markdown("""
    <style>
        body {
            background-color: #f5f5f5;
            color: #333333;
            font-family: 'Arial', sans-serif;
        }
        .stButton > button {
            background-color: #007bff;
            text-align: center;
            color: white;
            border-radius: 5px;
            padding: 10px 20px;
            font-size: 16px;
            border: none;
        }
        .stButton > button:hover {
            background-color: #0056b3;
        }
        .header {
            text-align: center;
            font-size: 40px;
            color: #4a4a4a;
            margin-bottom: 20px;
        }
        .footer {
            text-align: center;
            margin-top: 50px;
            font-size: 14px;
            color: #999999;
        }
        .h2 {
            text-align: center;
            margin-top: 50px;
            margin-bottom: 20px;
            color: #4a4a4a;
        }
        .h2_2 {
            text-align: center;
            margin-top: 20px;
            margin-bottom: 20px;
            color: #4a4a4a;
        }
    </style>
""", unsafe_allow_html=True)

# アプリのタイトル
st.markdown('<div class="header">🎨 明治時代の文化イメージ生成アプリ</div>', unsafe_allow_html=True)

st.markdown('<div class="h2">プロンプトの例を紹介します</div>', unsafe_allow_html=True)

st.markdown('<div class="h2_2">「煉瓦造りの洋風建築が立ち並ぶ街並み」</div>', unsafe_allow_html=True)

# ユーザー入力フォーム
user_input = st.text_input("あなたの明治時代のイメージを文章で入力してください(入力したものは自動で英訳されます):", "")

def translate_to_english(text):
    """日本語を英語に翻訳する関数"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Translate the following Japanese text into English."},
                {"role": "user", "content": text}
            ]
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        st.error(f"翻訳中にエラーが発生しました: {e}")
        return None

# レイアウトを中央揃え
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("画像を生成する ✨"):
        if user_input:
            try:
                with st.spinner("翻訳中...少々お待ちください！"):
                    english_prompt = translate_to_english(user_input)

                if english_prompt:
                    with st.spinner("画像を生成中...少々お待ちください！"):
                        # DALL·Eを使った画像生成
                        response = openai.Image.create(
                            model="dall-e-3",
                            prompt=english_prompt + " this beautiful painting is symbolic of the atmosphere of the Meiji Era (1868-1912) in Japan, a time of civilization and enlightenment where modernity and tradition coexisted",
                            n=1,
                            quality="standard",
                            size="1024x1024"
                        )
                        image_url = response["data"][0]["url"]
                    st.image(image_url, caption="生成された画像", use_container_width=True)
                else:
                    st.warning("翻訳に失敗しました。")
            except Exception as e:
                st.error(f"画像生成中にエラーが発生しました: {e}")
        else:
            st.warning("キーワードを入力してください！")

# フッター
st.markdown('<div class="footer">© 2025 明治イメージ生成アプリ - Powered by Streamlit & OpenAI</div>', unsafe_allow_html=True)
