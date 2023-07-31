
import sys
from gif_adder import GifConfig, set_editing_video
from transcribe import transcribe
import pandas as pd
import faiss
from sentence_transformers import SentenceTransformer
import torch

MAXIMUN_ACCEPTED_DISTANCE = 1.3

if __name__ == "__main__":
    video_path = sys.argv[1]
    set_editing_video(video_path)
    print("Generating transciption...")
    segments = transcribe(video_path)
    print("Loading databse...")
    gifs_database = faiss.read_index("data/gifs_dtb.index")
    gifs_urls = pd.read_table("data/urls.csv", index_col=False)

    transcption_texts = list(map(lambda x: x["text"], segments))
    model = SentenceTransformer('all-MiniLM-L6-v2')
    if torch.cuda.is_available():
        model = model.to(torch.device("cuda"))

    print("Embedding transciption...")
    embeddings = model.encode(transcption_texts, show_progress_bar=False)

    print("Getting matching gifs...")
    distances, matchs_gifs = gifs_database.search(embeddings, 1)
    matchs_gifs = matchs_gifs[:, 0]
    distances = distances[:, 0]

    matchs_gifs = gifs_urls.iloc[matchs_gifs]
    matchs_gifs = matchs_gifs.iloc[:, 0].values

    print("Editing video...")
    for segment, gif_url, distance in zip(segments, matchs_gifs, distances):
        start = segment["start"]
        end = segment["end"]
        duration = end-start
        text = segment["text"]

        if distance <= MAXIMUN_ACCEPTED_DISTANCE:
            current_gif = GifConfig.from_url(gif_url)
            if current_gif.length <= duration:
                current_gif.put_on_video_at(start + duration/2 - current_gif.length/2)

    

