# Recorded chants

The app plays a real recording for any prayer or mantra listed in `index.json`. Without one, it uses the phone's built-in Hindi voice.

To add a recording:

1. Save it here as an MP3 named after the prayer's `id` in `js/prayers.js`, for example `audio/shiva.mp3` for Om Namah Shivaya or `audio/hanuman-chalisa.mp3`.
2. List it in `index.json`:

   ```json
   {
     "shiva": "audio/shiva.mp3",
     "hanuman-chalisa": "audio/hanuman-chalisa.mp3"
   }
   ```

3. Increase `CACHE` in `sw.js` so installed apps pick up the change.

For japa mantras, record a single repetition. The counter's "Chant along" mode plays it again and again and counts each one. Keep files small (mono, 64 kbps is plenty) and only use recordings you made yourself or have permission to share.
