from tokenizers import (
    Tokenizer,
    models,
    pre_tokenizers,
    trainers,
    normalizers,
    decoders,
)

tokenizer = Tokenizer(models.BPE())

tokenizer.normalizer = normalizers.Sequence([normalizers.NFKC()])

tokenizer.pre_tokenizer = pre_tokenizers.ByteLevel(add_prefix_space=False)

tokenizer.decoder = decoders.ByteLevel()

trainer = trainers.BpeTrainer(
    vocab_size=8000, special_tokens=["<|endoftext|>", "<|pad|>", "<|unk|>"]
)

files = ["./data/clean_msale.txt"]
tokenizer.train(files, trainer)

tokenizer.save("amharic-tokenizer.json")

print("--- Test ---")
encoded = tokenizer.encode("ፈስ")
print("Encoded Token: ", encoded.tokens)

decoded = tokenizer.decode(encoded.ids)
print("Decoded: ", decoded)
