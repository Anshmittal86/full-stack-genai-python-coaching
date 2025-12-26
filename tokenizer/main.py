import tiktoken

# Encoding
encoder = tiktoken.encoding_for_model("gpt-5")
print("Vocab_size", encoder.n_vocab)
text = "Hello how are you"
tokenIds = encoder.encode(text)
print(f'TokenIDS: {tokenIds}')

#Decoding
decodedText = encoder.decode(tokenIds)
print(f'Decoded: {decodedText}')






