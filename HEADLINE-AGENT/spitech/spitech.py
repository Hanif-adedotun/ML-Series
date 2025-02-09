from spitch import Spitch
import os
# Remove all non-alphabetic characters and extra spaces
import re
from dotenv import load_dotenv
load_dotenv('.env')

os.environ["SPITCH_API_KEY"] = ""
client = Spitch()


# Read text from output_text.txt and remove asterisks
with open("output_text.txt", "r") as f:
    text = f.read()
# Remove asterisks and numbers from text
# Remove asterisks and numbers, replace newlines with spaces, and ensure proper sentence separation
text = text.replace("*", "").translate(str.maketrans('', '', '0123456789'))
text = text.replace("\n", ". ")  # Replace newlines with full stops and space
text = re.sub(r'\.{2,}', '.', text)  # Replace multiple dots with single dot
text = re.sub(r'[^a-zA-Z\s,.]', '', text)  # Keep letters, whitespace, commas and dots
text = re.sub(r'\s+', ' ', text)  # Normalize whitespace
text = text.strip()  # Remove leading/trailing whitespace

print(text)
# def split_text_into_chunks(text, word_limit=25):
#           """ 
#           Function to split a long web page into reasonable chunks
#           """
#           sentences=[sentence.strip() for sentence in text.split('.') if sentence.strip()]
#           chunks=[]
#           for sentence in sentences:
#                chunks.append(".")
#           sentence_splitted=sentence.split(" ")
#           num_words=len(sentence_splitted)
#           start_index=0
#           if num_words>word_limit:
#                while start_index<num_words:
#                     end_index=min(num_words,start_index+word_limit)
#                     chunks.append(" ".join(sentence_splitted[start_index:start_index+word_limit]))
#                     start_index=end_index
#           else:
#                chunks.append(sentence)
#           return chunks
     
# print("Splitting text into chunks...")     
# chunks=split_text_into_chunks(text)
# print(f"Total chunks to process: {len(chunks)}")

with open("news.wav", "wb") as f:
    response = client.speech.generate(
        text=" ".join(text.split()[:20]),
        language="en",
        voice="lucy"
    )
    f.write(response.read())
