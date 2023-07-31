gif_time=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 $2) 
s_time=$3
e_time=$(echo $s_time + $gif_time | bc)  
ffmpeg -y -i $1 -i $2 -filter_complex "[1]setpts=PTS-STARTPTS+$s_time/TB[top];[0:0][top]overlay=enable='between(t\,$s_time,$e_time)'[out]" -map [out] -map 0:a -c:a copy -c:v libx264 -preset veryfast $4
