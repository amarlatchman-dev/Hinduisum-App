# Recorded chants

The app plays a real recording for any prayer or mantra listed in `index.json`. Without one, it uses the phone's built-in Hindi voice.

## The published chants

Every prayer is recorded verse by verse in `audio/<id>/<verse>.mp3`, made with ElevenLabs text to speech by `scripts/build_audio.py` (the "Brian" voice on the Multilingual v2 model, slowed a little for chanting). `index.json` lists each prayer's clips in order:

```json
{ "ya-devi": ["audio/ya-devi/1.mp3", "audio/ya-devi/2.mp3", "audio/ya-devi/3.mp3", "audio/ya-devi/4.mp3"] }
```

The app plays them one after another and highlights each verse as it is chanted, also in Aarti mode and in the japa counter. To record a prayer again, delete its folder and run `python3 scripts/build_audio.py <id>` with an ElevenLabs key in `ELEVENLABS_API_KEY`. A new prayer added to `js/prayers.js` is recorded the same way.

## Adding your own recording

A recording of a whole prayer in one file can replace the published clips.

People can also record a prayer in the app itself (the **Record** card on every prayer page). That recording plays only on their own device, ahead of any published one. **Share or send** exports it as a file named after the prayer's id, for example `hanuman-chalisa.webm` or `shiva.m4a`, which is ready to publish here. Converting it to MP3 first keeps it playable everywhere:

```sh
ffmpeg -i hanuman-chalisa.webm -ac 1 -b:a 64k audio/hanuman-chalisa.mp3
```

To add a recording:

1. Save it here as an MP3 named after the prayer's `id` in `js/prayers.js`, for example `audio/shiva.mp3` for Om Namah Shivaya or `audio/hanuman-chalisa.mp3`.
2. List it in `index.json` in place of the prayer's list of clips:

   ```json
   {
     "shiva": "audio/shiva.mp3",
     "hanuman-chalisa": "audio/hanuman-chalisa.mp3"
   }
   ```

3. Increase `CACHE` in `sw.js` so installed apps pick up the change.

For japa mantras, record a single repetition. The counter's "Chant along" mode plays it again and again and counts each one. Keep files small (mono, 64 kbps is plenty) and only use recordings you made yourself or have permission to share.
