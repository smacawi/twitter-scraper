import gensim.downloader as api
import pickle
model = api.load("glove-twitter-25")

# read file
file = open('EnvCanadaGloss.txt', 'rb')
lines = file.read().splitlines()
lines[0] = lines[0][3:]
lines = lines[:-1]
print(lines)

# tokenize the file lines
def create_embeddings(list_o_lines):
    tokens = []
    for line in list_o_lines:
        token = [t for t in line.replace("/", " ").replace("\"", " ").split(" ") if (t[0]!="(" and t[-1]!=")")]
        token = [t.lower() for t in token]
        tokens.append(token)
        print(token)
    return tokens

tokenz = create_embeddings(lines)

# generate embeddings for tokens

tot = {}
for ts in tokenz:
    emb = []
    for t in ts:
        try:
            emb.append(model[t])
        except Exception as e:
            print(e.__str__())
    # average embeddings across lines
    average = [sum(elements)/len(elements) for elements in zip(*emb)]
    tot[" ".join(ts)] = average

pickle.dump(tot, open("saveEmbeddings.pkl", "wb"))
# k-means cluster the embeddings

