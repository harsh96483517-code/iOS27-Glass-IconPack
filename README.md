# iOS 27 Glass IconPack

`input/` ke har icon ko upscale + iOS-27 glass effect, phir ek install-karne-wala **Android icon pack APK**.

## APK kahan milega
1. **Releases** tab: har push par naya `build-<n>` release + `iOS27-Glass-IconPack.apk` (seedha download link).
2. **Actions** tab -> run kholo -> Artifacts -> `iOS27-GlassIconPack-apk`.

## GitHub par kaise chalayein
1. Repo ki `main` branch par push karo — *IconPack APK* job khud chal jayegi (~10-15 min).
2. 4K PNG chahiye to **Actions** -> *Build Glass Icons + IconPack APK* -> **Run workflow**,
   `four_k` = true (aur `size` = 4096). Yeh alag job hai, isliye APK ka wait nahi karna padta
   (74 icons 4K par 1-2 ghante lete hain; jaldi test ke liye `size` = 1024 do).

## Local chalana
```
pip install pillow numpy opencv-contrib-python-headless
python tools/glass.py --input input --output out --size 1024 --sr
python tools/make_iconpack.py
gradle assembleDebug
```
`glass.py` resume-safe hai: dobara chalane par bane hue icon skip hote hain.
`--sr` AI upscaler (FSRCNN x4) try karta hai, na mile to Lanczos use hota hai.
APK ke andar icons 512px par save hote hain, isliye source 1024px kaafi hai.

## Apna icon badalna / add karna
`input/` me naya PNG (square) daalo, `mapping.csv` me ek row jodo.

## Launcher me apply karna (zaroori)
Icon pack app-wise tab hi auto-apply hota hai jab `mapping.csv` me `package` **aur** `component` ho.
Abhi sirf kuch known apps (Play Store, Chrome, Gmail, Maps, YouTube, WhatsApp, Snapchat, Google,
OneDrive, Flipkart, Instagram, PhonePe, ChatGPT, Claude, ZArchiver, Gemini) mapped hain.
Baaki ke liye component nikalo:
```
adb shell cmd package resolve-activity --brief <package.name>
```
aur `mapping.csv` me bharo. Bina mapping ke bhi Nova/Lawnchair me icon manually pick kar sakte ho
(icon pack ke andar sab icons dikhte hain).
