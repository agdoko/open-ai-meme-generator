import streamlit as st
import openai
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import requests
from dotenv import load_dotenv
import os

load_dotenv()
client = openai.OpenAI(api_key = os.getenv("OPENAI_API_KEY"))

st.title("Dragonball Z Meme Generaotr")

user_prompt = st.text_input("Enter your meme idea (e.g., 'Late for school')", "")

if st.button("Make my Meme"):
    if user_prompt:
        try:
            # Enhanced system prompt
            system_prompt = """You are a creative and hilarious meme generator powered by OpenAI.
                Your task is to create short, impactful meme captions and a vivid image description for DALL-E 3 based on the user's input.
                It is essential that the image you generate comes from the Dragon Ball Z anime universe. Your visual scenario should reflect well known scenes from Dragon Ball Z TV series or movies, such as epic battles, Super Saiyan transformations, or adventures on Namek. Likewise, your funny text needs to turn the user's initial prompt into a funny twist that is thematically related to well-known moments from the show.
                But adapt it to Dragon Ball Z: make the boyfriend Goku, the girlfriend Chi-Chi, and the distracting woman Bulma, with 'top_text' like 'WHEN YOU HAVE A GF' and 'bottom_text' like 'BUT POWER LEVELS CALL'. And you also need to use the humouristic structures and meme formats
                of the most common internet memes. To do this, first select the most relevant meme format from the following catalogue of top 30 common internet memes (described below), based on how well it fits the user's input thematically or humorously. Then, adapt that meme's structure to a Studio Ghibli anime style scenario.

                Catalogue of top 30 common internet memes with text descriptions:
                1. Distracted Boyfriend - A man looking at another woman while his girlfriend looks on in shock, representing temptation or distraction.
                2. Success Kid - A baby on the beach with a fist pump, symbolizing small victories or determination.
                3. This Is Fine - A dog in a burning room drinking coffee, depicting denial in chaotic situations.
                4. Expanding Brain - A series of brain images showing increasing levels of intelligence or complexity in ideas.
                5. Drake Hotline Bling - Drake rejecting one option and approving another, for preferences or comparisons.
                6. Roll Safe - A guy pointing to his head with the caption "Think about it," for clever advice or warnings.
                7. Confused Math Lady - A woman with math equations around her head, representing confusion or overthinking.
                8. Blinking White Guy - A man blinking in surprise, for moments of realization or disbelief.
                9. Woman Yelling at Cat - A woman yelling at a confused cat at a dinner table, for arguments or contrasts.
                10. Change My Mind - A guy at a table with a sign saying "Change My Mind," for challenging opinions.
                11. Mocking SpongeBob - Text in alternating case mocking something, often childish or sarcastic.
                12. Evil Kermit - Kermit the Frog talking to his dark hooded self, representing internal moral conflicts.
                13. Surprised Pikachu - Pikachu with a surprised face, for obvious outcomes that shock anyway.
                14. American Chopper Argument - Father and son arguing intensely, for heated debates.
                15. Is This a Pigeon? - An anime character misidentifying a butterfly as a pigeon, for misunderstandings.
                16. One Does Not Simply - Boromir from LOTR saying "One does not simply walk into Mordor," for things that are not easy.
                17. The Most Interesting Man in the World - Dos Equis guy saying "I don't always..., but when I do...," for rare actions.
                18. Y U No - A rage comic guy yelling "Y U No [do something]?", for frustrations.
                19. Bad Luck Brian - A kid with braces experiencing constant bad luck in captions.
                20. First World Problems - A woman crying over minor inconveniences in a privileged context.
                21. Philosoraptor - A dinosaur pondering deep philosophical questions.
                22. Ermahgerd - A girl excitedly holding books with exaggerated speech like "Ermahgerd Berks!"
                23. Scumbag Steve - A guy in a hat doing selfish or scummy things in captions.
                24. Good Guy Greg - A guy in a beanie doing kind or helpful things.
                25. Grumpy Cat - A cat with a grumpy expression saying "No" or negative captions.
                26. Doge - A Shiba Inu dog with broken English captions like "such wow, very meme."
                27. Rickroll - Tricking someone into watching Rick Astley's "Never Gonna Give You Up" video.
                28. Pepe the Frog - A green frog with various sad, smug, or angry expressions.
                29. Harambe - A gorilla from a zoo incident, symbolizing internet outrage or remembrance.
                30. Arthur Fist - Arthur from the cartoon clenching his fist in anger.

                Example of what I mean: If the user prompted something along the lines of 'break up', you might select the Distracted Boyfriend meme structure where a character is distracted by something else while with their partner. But adapt it to Studio Ghibli: make the boyfriend Howl from Howl's Moving Castle, the girlfriend Sophie, and the distracting woman a spirit from Spirited Away, with 'top_text' like 'WHEN YOU HAVE A GF' and 'bottom_text' like 'BUT MAGIC CALLS'.

                Instructions:
                1. Generate 'top_text' and 'bottom_text' for a classic meme (like Impact font style, short, punchy, max 10 words each, all caps for emphasis).
                2. Create an 'image_prompt' for DALL-E 3 (50-100 words, Dragon Ball Z anime style, avoid NSFW content, but it can be funny and playful, use the selected internet meme format stylized to Dragon Ball Z theme).
                3. Output in JSON format: {"top_text": "...", "bottom_text": "...", "image_prompt": "..."}
                """
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=1.2
            )
            import json
            data = json.loads(response.choices[0].message.content)
            top_text = data['top_text']
            bottom_text = data['bottom_text']
            image_prompt = data['image_prompt']

            st.write(f"Generated Captions: Top - {top_text} | Bottom - {bottom_text}")

            image_response = client.images.generate(
                model="dall-e-3",
                prompt=image_prompt,
                n=1,
                size="1024x1024"
            )
            image_url = image_response.data[0].url
            image_data = requests.get(image_url).content
            base_image = Image.open(BytesIO(image_data))

            draw = ImageDraw.Draw(base_image)
            try:
                font = ImageFont.truetype("impact.ttf", size=60)  # Meme-style font, 5x larger
            except IOError:
                font = ImageFont.load_default(size=60)  # Fallback to larger default font
            width, height = base_image.size
            bbox = draw.textbbox((0, 0), top_text, font=font)
            tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
            draw.text(((width - tw) / 2, 10), top_text, fill="white", font=font, stroke_width=8, stroke_fill="black")
            bbox = draw.textbbox((0, 0), bottom_text, font=font)
            bw, bh = bbox[2] - bbox[0], bbox[3] - bbox[1]
            draw.text(((width - bw) / 2, height - bh - 20), bottom_text, fill="white", font=font, stroke_width=8, stroke_fill="black")
            st.image(base_image, caption="Your OpenAI Meme!")

            buffered = BytesIO()
            base_image.save(buffered, format="PNG")
            st.download_button("Download Meme", data=buffered.getvalue(), file_name="openai_meme.png", mime="image/png")

        except Exception as e:
            st.error(f"Oops! Error: {str(e)} (Check API key or limits)")
    else:
        st.write("Enter an idea first!")
