# Note: The openai-python library support for Azure OpenAI is in preview.
import os
import openai
import pandas as pd
openai.api_type = "azure"
openai.api_base = "https://reviewscons.openai.azure.com/"
openai.api_version = "2022-12-01"
openai.api_key = os.getenv("OPENAI_API_KEY")

df = pd.read_csv("./data/Datafiniti_Hotel_Reviews.csv")
df_10 = df.head(10)

reviews = {}
for index, headers in df_10.iterrows():
    review_content = str(headers["reviews.text"])
    name = str(headers["name"])
    existing_review = reviews.get(name)
    if existing_review == None:
        reviews[name] = review_content    
    else: 
        reviews[name] = existing_review + review_content
    

for key, value in reviews.items():
    review_content_string = value;
    response = openai.Completion.create(
        engine="ReviewSummary",
        prompt="Summarize the following review content in 100 words" + review_content_string + "\n\nSummary:",
        temperature=0.3,
        max_tokens=250,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        best_of=1,
        stop=None)
    generated_text = response.choices[0].text.strip()
    print(key)
    print(generated_text)
    print("\n\n")
