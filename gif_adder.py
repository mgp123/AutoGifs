from subprocess import check_output, call
import os
import subprocess
import urllib.request

video_path=None

def set_editing_video(new_video_path):
    global video_path
    video_path=new_video_path

class GifConfig:
    def __init__(self, gif_path) -> None:
        self.gif_path = gif_path
        self.resize()
        self.length = self.get_length()
    
    def from_url(url, save_path="temp.gif"):
        urllib.request.urlretrieve(url, "temp.gif")
        return GifConfig(save_path)
    
    def resize(self):
        call(f"bash resize.sh {self.gif_path} resized.gif", shell=True)
        os.remove(self.gif_path)
        os.rename("resized.gif", self.gif_path) 

    def get_length(self) -> float:
        s = check_output(f"bash get_time.sh {self.gif_path}", shell=True)
        return float(s)
    
    def put_on_video_at(self,timestamp:float, out_path:str="output.mp4", update_video_path=True ) -> None:
        call(f"bash add_gif.sh {video_path} {self.gif_path} {timestamp} temp.mp4", shell=True, stdout=subprocess.DEVNULL)
        
        # this thingy is to avoid ffmpeg in place errors
        os.remove(out_path)
        os.rename("temp.mp4", out_path) 
        
        if update_video_path:
            set_editing_video(out_path)


