#import some important packages 
import os
import re
import json
import torch
import inflect
import random
import uroman as ur
import numpy as np
import torchaudio
import IPython
from transformers import AutoModelForCausalLM, AutoTokenizer
from yarngpt.audiotokenizer import AudioTokenizer

# model path and wavtokenizer weight path (the paths are assumed based on Google colab, a different environment might save the weights to a different location).
hf_path="saheedniyi/YarnGPT"
wav_tokenizer_config_path="./content/wavtokenizer_mediumdata_frame75_3s_nq1_code4096_dim512_kmeans200_attn.yaml"
wav_tokenizer_model_path = "./content/wavtokenizer_large_speech_320_24k.ckpt"

print("Initializing AudioTokenizer...")
# create the AudioTokenizer object 
audio_tokenizer=AudioTokenizer(
    hf_path,wav_tokenizer_model_path,wav_tokenizer_config_path
)

print("Loading model weights...")
#load the model weights
model = AutoModelForCausalLM.from_pretrained(hf_path,torch_dtype="auto").to(audio_tokenizer.device)

print("Reading and processing input text...")
# your input text
# text="Uhm, so, what was the inspiration behind your latest project? Like, was there a specific moment where you were like, 'Yeah, this is it!' Or, you know, did it just kind of, uh, come together naturally over time?"
# Read text from output_text.txt and remove asterisks
with open("output_text.txt", "r") as f:
    text = f.read()
text = text.replace("*", "")

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

def split_text_into_chunks(text, word_limit=50):
          """ 
          Function to split a long web page into reasonable chunks
          """
          sentences=[sentence.strip() for sentence in text.split('.') if sentence.strip()]
          chunks=[]
          for sentence in sentences:
               chunks.append(".")
          sentence_splitted=sentence.split(" ")
          num_words=len(sentence_splitted)
          start_index=0
          if num_words>word_limit:
               while start_index<num_words:
                    end_index=min(num_words,start_index+word_limit)
                    chunks.append(" ".join(sentence_splitted[start_index:start_index+word_limit]))
                    start_index=end_index
          else:
               chunks.append(sentence)
          return chunks
     
print("Splitting text into chunks...")     
chunks=split_text_into_chunks(text)
print(f"Total chunks to process: {len(chunks)}")

#Looping over the chunks and adding creating a large `all_codes` list
all_codes=[]
for i,chunk in enumerate(chunks):
  print(f"\nProcessing chunk {i+1}/{len(chunks)}")
  print("-"*40)
  print(f"Chunk content: {chunk}")
  if chunk==".":
    print("Adding pause for full stop...")
    #add silence for 0.25 seconds if we encounter a full stop
    all_codes.extend([453]*20)
  else:
    print("Generating audio codes...")
    prompt=audio_tokenizer.create_prompt(chunk,"chinenye")
    input_ids=audio_tokenizer.tokenize_prompt(prompt)
    output  = model.generate(
            input_ids=input_ids,
            temperature=0.1,
            repetition_penalty=1.1,
            max_length=4000,
        )
    codes=audio_tokenizer.get_codes(output)
    all_codes.extend(codes)
    print(f"Added {len(codes)} audio codes")

print("\nAll chunks processed. Generating final audio...")
# Converting to audio
audio=audio_tokenizer.get_audio(all_codes)
print(f"Audio generated with {len(audio)/24000:.2f} seconds duration")

print("Playing audio preview...")
IPython.display.Audio(audio,rate=24000)

print("Saving audio file...")
torchaudio.save(f"news1.wav", audio, sample_rate=24000)
print("Audio generation complete! File saved as news1.wav")
