from spitch import Spitch
import os
# Remove all non-alphabetic characters and extra spaces
import re
from dotenv import load_dotenv
load_dotenv('.env')

os.environ["SPITCH_API_KEY"] = "sk_vdfGhhieS312CtTtnN89jnuWilTFxHEfXFkZmIZ5"
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

with client.speech.with_streaming_response.generate(
    text=text,
    language="en",
    voice="john"
) as response:
    response.stream_to_file("news-latest.wav")