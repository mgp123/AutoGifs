import numpy as np
from sentence_transformers import SentenceTransformer
import pandas as pd
import torch
import faiss


model = SentenceTransformer('all-MiniLM-L6-v2')
if torch.cuda.is_available():
   model = model.to(torch.device("cuda"))

# this comes from a dataset of tumblr gifs
# you'll have to download it yourself if you want to regenerate the embeddings
df = pd.read_table("local/gifs/data/tgif-v1.0.tsv")

sentences = df.iloc[:, 1].values

embeddings = model.encode(sentences, show_progress_bar=True)
embeddings = np.array([embedding for embedding in embeddings]).astype("float32")
vdtb = faiss.IndexFlatL2(embeddings.shape[1])
vdtb = faiss.IndexIDMap(vdtb)
vdtb.add_with_ids(embeddings, range(len(df)))
faiss.write_index(vdtb, "data/gifs_dtb.index")
urls=df.drop(df.columns[1], axis=1)
urls.to_csv("data/urls.csv", index=False)
