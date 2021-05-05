# Useful Tools

### Convert PDF to TXT
```shell
$ pdftotext <infile> # installed by default in Ubuntu/Wasta
```

### Convert ODT to TXT
```shell
$ sudo apt install odt2txt
$ odt2txt --output=<outfile> <infile>
```

### Change video speed (maintain audio pitch)
```bash
speed=0.8   # 80% of the original speed, 1.25x the video length
inv=1.25    # inverse of $speed, used to correct the audio pitch
$ ffmpeg -i input.mp4 -filter:v 'setpts='$speed'*PTS' -filter:a 'atempo='$inv'' ouput.mp4
```
