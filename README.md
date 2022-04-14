# VideoPipeline[name pending]

This is a way to complex project that achieves almost nothing new i fear. 

## *Current Status:* Research & Development

### The Problem:

I do some Youtube Videos on the site, mostly Lets Plays and very rare Tutorial / Introduction ones. I never made it big with those videos and my life goes on but i still greatly enjoy working for a smaller audience. A big hog on my time is the process between recording (the fun part) and releasing on Youtube. The breakdown is as follows:

1. extracting audio tracks with MKVextract / MeGUI
2. clicking through two menus in the by now ancient MeGUI
3. waiting for MeGUI to finish extracting, clicking ok, adding the new video to the queue, hoping nothing breaks (*annoying bug where it actually adds the wrong file in the queue*)
4. import two audio tracks into audacity, mix up the volume (same for the whole record session)
5. mux the whole thing with MKVtoolnix (also adding the raw separated tracks as additional audio just in case, Youtube throws them away but i allows me to redo the mix if necessary as long as i store those files)
6. upload to Youtube

This takes quite a long time as there are small pauses between the phases which creates an annoying effect where i cannot really do anything else while this goes on.

### The Idea:

We got ffmpeg, a mighty powerful tool that can do everything we want if we know the right magic words and ask nicely. A small GUI, some in-build scheduling, some presets and a huge amount of logic to allow tired me to do the job flawlessly should do the trick. And yes, i am aware of the existence of Handbrake, still, some clicks required. And then there is this stupid requirement of mine to archive the two original tracks in the file as well, a function no one seems to have implemented n their program (Handbrake has it kinda). Which might be because additional audio tracks are usually meant to be used for other languages. Anyway, here is my initial foray into the world of ffmpeg parameters, the audio mixing is not entirely there but for the moment this does exactly what i want.

#### Code Snippets

```bash
ffmpeg -i Kotor2\ 73_30s-021.mkv \
	-filter_complex '[0:a:1][0:a:2]amix=2:longest:weights=1 2[aout]' \
	-map 0:v:0 -c:v:0 libx264 -crf 22.5 -preset medium -g 250 -bf 16 \
	-map "[aout]" -c:a libvorbis -q:a 7 \
	-map 0:a:1 \
	-map 0:a:2 \
	"output.mkv"
```

### Tooling

I have some experience with Pyside2/Qt therefore i will use Pyside6. (Leaps of logic here). I actually played with the thought of using [DearPyGui](https://github.com/hoffstadt/DearPyGui) but i have experience with Qt and this project is GPLv3 anyway, so i choose the path of least resistance. (Also, there are more answers on Stackoverflow about Qt in general).

There is a library to use *ffmpeg* in python that abstracts some of the function calls, unfortunately the author did not saw me coming and my niche needs. Anyway, he abstracts *ffprobe* for me which i also want, so i am using what he got.

## Planning

A scribbled a lot of notes on an A2 piece of paper getting something resembling a project plan. Good old waterfall, as i am product owner, developer and everything at once we might get away with it.

1. **Phase 1**
   * All encoding on one device, no copy process
   * Qt based interface, no headless mode
   * Schedule & Queue logic
   * Progress bar (a kinda important thing)
   * Convenience menus for editing presets
2. **Phase 2**
   * Synchronise Settings / Profiles between agents / federated swarm
   * Synchronise Schedule among Agents
   * Episode based renaming
3. **Optional Stuff / Ideas**
   * different encoder options (changes parameter selection)
   * multiple encoder stations, parallel workings according to bottlenecks 
   * external monitoring / api interface
   * a stupid phone app to get that data on android (i have zero experience with that, kivy?)

This plan mentions some things i haven't yet explained. More words then. As of now my residential internet has some limits and it turns out that some material gets BIG, usually its fast gameplay in 1440P and 60fps, looks awesome, kinda unwieldy. As my current gaming pc has a RTX3080 and a Ryzen 5800x its best equipped to do the encoding and recording but the internet connection bottlenecks and every hour the pc is running and not doing useful things it pummels onto my electrical bill which might be significant, especially where i live. Fortunately i already have a personal NAS/Local Server that runs 24/7 and is optimised to not devour more than 20 Watts (should probably be lower but its a DIY one). I am yet unsure how to transfer data on that machine, i might either use some kind of *shutil*, use the samba shares that already exist, spin up a local ftp server or just do it with a direct connection (which means i have to develop a data transfer protocol right?)

### foreseeable problems (*cough* challenges)

* traditionally, Google and Youtube dont like it when you mass upload stuff via API, i have to do another foray into the API but iirc, uploading costs a lot of points, i might have to do this step by hand and just spin up a small desktop environment on the server (well, i guess i could use selenium but this sounds fragile at its best)
* the thought of using a federated network of independent agents that synchronize their settings and projects status sounds a lot like reinventing active directory, which is...a lot, all i want is to easily put videos of me playing/commenting on games on youtube
* i solved the progress bar / async call thing with Qt already as there is a signalling backend i can leverage, my experience with asynchronous calls in general is very limited, i guess this will be a slow progress area
* interface design, i am an engineer, not an artsy person
* interface logic that does not result in unstable/unusable states, needs some fine handling of the situation, might be tiresome to get it just right
* spaghetti code, this is my fourth project where i try to keep a somewhat clear package structure and i still feel like i am a child in big boots.
* find a bloody name for the thing, 70% chance that "VideoPipeline" will be it (Leonardo of Quirm called and wants his quirks back)