import numpy as np
from tokenizers import Tokenizer, decoders
from gensim.models import FastText
import logging

logging.basicConfig(
    format="%(asctime)s : %(levelname)s : %(message)s", level=logging.INFO
)


def get_word_vector(word, tokenizer, model):
    tokens = tokenizer.encode(word).tokens

    # 2. Average or sum the vectors of all subwords in the word
    vectors = [model.wv[t] for t in tokens if t in model.wv]
    if len(vectors) == 0:
        return np.zeros(model.vector_size)

    return np.mean(vectors, axis=0)


bpe_tokenizer = Tokenizer.from_file("./amharic-tokenizer.json")
Tokenizer.decoder = decoders.ByteLevel()
cleaned_corpus = []

with open("./data/clean_msale.txt", "r", encoding="utf-8") as in_file:
    for line in in_file:
        tokens = bpe_tokenizer.encode(line).tokens
        cleaned_corpus.append(tokens)

# Train the model
# window: context window size (how many words before/after to look at)
# min_count: ignore words that appear less than this many times
print("Training model...")
model = FastText(
    sentences=cleaned_corpus,
    vector_size=256,
    window=5,
    min_count=2,
    workers=4,
    epochs=20,
)

model.save("amharic_fasttext.model")
print("Training complete!")

print("--- Test ---")
print("ፈስ - ሴት + ዝላይ =")

v_fes = get_word_vector("ፈስ", bpe_tokenizer, model)
v_set = get_word_vector("ሴት", bpe_tokenizer, model)
v_zlay = get_word_vector("ዝላይ", bpe_tokenizer, model)

target_vector = v_fes - v_set + v_zlay

closest_tokens = model.wv.most_similar(positive=[target_vector], topn=3)

for word, similarity in closest_tokens:
    print(f"{bpe_tokenizer.decoder.decode([word])}: {similarity}")
