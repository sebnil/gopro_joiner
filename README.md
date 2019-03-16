GoPro joiner python script
======
**gopro_joiner** is a script to combine, rename and compress gopro videos. It is just something I hacked together because the file naming convention from GoPro is quite messed up.
The script will also run ffmpeg on the files to combine the videos to compress them. 

```
$ python ./joiner path/to/video_folder
```

## Examples
### Just combine
You have two GoPro video session. One is in three chapters, and the other one is just one chapter like this:
- GH010073.MP4 (video 1 chapter 1)
- GH010074.MP4 (video 2 chapter 1)
- GH020073.MP4 (video 1 chapter 2)
- GH030073.MP4 (video 1 chapter 3)

Run the script in the folder:
```
$ python ./joiner path/to/video_folder
```
The script will output video files:
- GH010073_combined.MP4
- GH010074_combined.MP4

### Combine and compress
If you want to combine and compress just add scale and fps arguments like so:
```
$ python ./joiner path/to/video_folder --scale hd720 --fps 25
```
```
$ python ./joiner path/to/video_folder --scale hd1080 --fps 60
```
```
$ python ./joiner path/to/video_folder --scale 2k --fps 60
```
```
$ python ./joiner path/to/video_folder --scale 4k --fps 30
```
And so on..

### Support my creation of open source software:
[![Flattr this git repo](http://api.flattr.com/button/flattr-badge-large.png)](https://flattr.com/submit/auto?user_id=sebnil&url=https://github.com/sebnil/gopro_joiner)

<a href='https://ko-fi.com/A0A2HYRH' target='_blank'><img height='36' style='border:0px;height:36px;' src='https://az743702.vo.msecnd.net/cdn/kofi2.png?v=0' border='0' alt='Buy Me a Coffee at ko-fi.com' /></a>
