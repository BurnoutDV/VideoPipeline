# Project_Name

## Code Snippets

```bash
ffmpeg -i Kotor2\ 73_30s-021.mkv \
	-filter_complex '[0:a:1][0:a:2]amix=2:longest:weights=1 2[aout]' \
	-map 0:v:0 -c:v:0 libx264 -crf 22.5 -preset medium -g 250 -bf 16 \
	-map "[aout]" -c:a libvorbis -q:a 7 \
	-map 0:a:1 \
	-map 0:a:2 \
	"output.mkv"
```