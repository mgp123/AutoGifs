# AutoGifs
AutoGifs is a small script that automatically adds GIFs to a video, corresponding to what the speaker is saying. It was hacked in more or less an afternoon, so it's pretty bare bones. AutoGifs is not meant to be the next groundbreaking technology or a high-end video production tool. It's just a small thing

## An example
![](https://github.com/mgp123/AutoGifs/raw/master/sample/output.mp4)


## How It Works
1. **Transcription with Whisper**: AutoGifs utilizes the powerful `whisper` library to transcribe the audio content of the video.

2. **Embedding of Segment**: Each segment is then embedded into a numerical representation that captures its essence and meaning.

3. **GIF Caption Embeddings**: The heart of AutoGifs lies in using a collection of GIFs, each with its own caption. The dataset is taken from [Tumblr GIF (TGIF) dataset](https://github.com/raingo/TGIF-Release/tree/master/code/gif2txt-lstm). The captions are embedded into vectors, forming a database of GIF embeddings. The `faiss` library is used for the vector database.

4. **Smart Matching**: It matches each segmented text to the most relevant GIF caption by comparing their respective embeddings.

## Limitations

- Transcription accuracy depends on the quality of the audio input. Background noise or unclear speech may affect the results.

- Currently, the stitching of the GIFs is done sequentially using ffmpeg. Saving into a file each time. This makes them EXTREMELY SLOW. Most of the compute time is spent here. Should definitely change that. 

- The current matching between text and GIFs is pretty naive. Thus, the connection between the GIF and the video is shaky at best. It doesn't follow much of the meaning related to the context. This could probably improve with better embeddings and a more custom search.

- The dataset is a bit old (2015) so the GIFs are out of date

## A Note on this editing trick
While AutoGifs was a fun experiment, I must admit that I personally don't have any affinity for this editing trick. I believe it may somewhat diminish the impact of the content and border on the tacky side. 

## TODO
- Improve GIF stitching for faster processing.
- Enhance GIF matching algorithm for smarter and more accurate matches.
