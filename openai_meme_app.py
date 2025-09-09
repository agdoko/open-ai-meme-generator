import streamlit as st
import openai
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import requests
from dotenv import load_dotenv
import os

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

st.title("Pokemon Meme Generaotr")

user_prompt = st.text_input("Enter your meme idea (e.g., 'Late for school')", "")

if st.button("Make my Meme"):
    if user_prompt:
        try:
            # Enhanced system prompt
            system_prompt = """You are a creative and hilarious meme generator powered by OpenAI.
            Your task is to create short, impactful meme captions and a vivid image description for DALL-E 3 based on the user's input.
            It is essential that the image you generate comes from the tv and video game pokeomon universe. Your visual scenario should
            reflect well known scenes from the pokemon tv show or from the video games. Likewise, your funny text needs to turn the user's
            initial prompt into a funny twist that is thematically related to well-known moments from the show. And you also need to use the humouristic structures and meme formats
            of the most common internet memes. Let me give you an example of what I mean: If the user prompted
            something along the lines of 'break up' you might use the well-known annoyed girlfriend meme structure
            where a couple is walking and the boyfriend is caught by his annoyed girlfriend staring at an attractive women walking past. But you instead make the boyfriend Ash Ketchum
            and the girlfriend is squirtle and the attractive woman walking past is blastoise and the 'top_text' might be 'when you have a gf' and the 'bottom_text' might be 'but you want more spice'

                Instructions:
                1. Generate 'top_text' and 'bottom_text' for a classic meme (like Impact font style, short, punchy, max 10 words each, all caps for emphasis).
                2. Create an 'image_prompt' for DALL-E 3 (50-100 words, pokemon anime style, avoid NSFW content, but it can be funny and playful, use common internet meme formats that are stylised to pokemon theme).
                3. Output in JSON format: {"top_text": "...", "bottom_text": "...", "image_prompt": "..."}

                """
            response = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=1.2
            )
            import json
            data = json.loads(response.choices[0].message['content'])
            top_text = data['top_text']
            bottom_text = data['bottom_text']
            image_prompt = data['image_prompt']

            st.write(f"Generated Captions: Top - {top_text} | Bottom - {bottom_text}")

            image_response = openai.Image.create(
                model="dall-e-3",
                prompt=image_prompt,
                n=1,
                size="1024x1024"
            )
            image_url = image_response['data'][0]['url']
            image_data = requests.get(image_url).content
            base_image = Image.open(BytesIO(image_data))

            draw = ImageDraw.Draw(base_image)
            font = ImageFont.truetype("arial.ttf", size=60)  # Download impact.ttf for better meme style
            width, height = base_image.size
            tw, th = draw.textsize(top_text, font=font)
            draw.text(((width - tw) / 2, 10), top_text, fill="white", font=font, stroke_width=3, stroke_fill="black")
            bw, bh = draw.textsize(bottom_text, font=font)
            draw.text(((width - bw) / 2, height - bh - 20), bottom_text, fill="white", font=font, stroke_width=3, stroke_fill="black")

            st.image(base_image, caption="Your OpenAI Meme!")

            buffered = BytesIO()
            base_image.save(buffered, format="PNG")
            st.download_button("Download Meme", data=buffered.getvalue(), file_name="openai_meme.png", mime="image/png")

        except Exception as e:
            st.error(f"Oops! Error: {str(e)} (Check API key or limits)")
    else:
        st.write("Enter an idea first!")
