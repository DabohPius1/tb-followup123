# TB Follow-up Calculator — Android

This is a Python/Kivy Android app for calculating and saving TB patient follow-up dates.

Schedule:
- Month 2: treatment start date + 56 days
- Month 5: treatment start date + 140 days
- Month 6: treatment start date + 168 days

Features:
- Patient name
- Patient ID
- Treatment start date (DD-MM-YYYY)
- Automatic follow-up dates
- Local offline storage
- Saved patient records
- Delete records

## Build the APK

Use Linux/WSL with Buildozer.

1. Install the required Android build environment.
2. Open this project folder.
3. Run:

   buildozer -v android debug

The APK will be created in the `bin/` directory.

For a release APK, configure signing and use the appropriate release build process.

## Build with GitHub (no PC setup needed)

1. Upload ALL files to the ROOT of a GitHub repo (main.py and buildozer.spec must
   be at the top level, not inside a sub-folder). Include the hidden folder
   .github/workflows/build-apk.yml.
2. Open the repo > Actions tab > "Build Android APK" > Run workflow.
3. Wait 20-40 min (first build). Download "tb-followup-apk" from the run's Artifacts.
