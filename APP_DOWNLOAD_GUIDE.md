# 📱 Calories Calculator - App Downloads

Two separate native apps + web version, all automated on GitHub Actions.

---

## 🤖 Android App (APK)

**Latest Build:** Run #12 ✅

**Download Link:**
https://github.com/san1eev1/calories-calculator/actions/runs/35262720231

**Installation:**
1. Download `android-app` artifact (contains `.apk`)
2. Transfer APK to your Android phone
3. Open file manager → Tap APK → Install
4. Open "Tiffin" app on your phone

**What's inside:**
- Native Android app
- Stores data locally on device
- Ready for Google Play Store submission
- Full nutrition tracking: 44 nutrients, barcode scanning, meal logging

---

## 🍎 iOS App (IPA)

**Latest Build:** Run #12 ✅

**Download Link:**
https://github.com/san1eev1/calories-calculator/actions/runs/35262720230

**Installation (choose one):**

**Option 1: AltStore (Recommended)**
- Download: https://altstore.io
- Install on Mac
- Connect iPhone → Add IPA via AltStore
- Takes 5 minutes

**Option 2: Apple Configurator 2 (Free)**
- Download from Mac App Store
- Connect iPhone via cable
- Drag & drop IPA onto window

**Option 3: Sideloadly**
- Download: https://sideloadly.io
- Connect iPhone
- Drag IPA onto app

**What's inside:**
- Native iOS app for iPhone
- Stores data locally on device
- Ready for TestFlight/App Store submission
- Full nutrition tracking: 44 nutrients, barcode scanning, meal logging

---

## 🌐 Web Version

**Download:** Get `web-app` artifact from same GitHub Actions run

**Usage:**
- Open `tiffin.html` in any browser
- Works on phone browser too
- No installation needed
- Data syncs with localStorage

---

## 🔄 Automatic Updates

Both apps rebuild **automatically** whenever you push to `claude/friendly-davinci-kz02xp` branch.

**To get latest version:**
1. Go to: https://github.com/san1eev1/calories-calculator/actions
2. Open latest successful build
3. Download updated artifact

---

## 📊 App Status

| App | Platform | Status | Build Time | Size |
|-----|----------|--------|-----------|------|
| Android | APK | ✅ Ready | ~2-3 min | ~50MB |
| iOS | IPA | ✅ Ready | ~1-2 min | ~40MB |
| Web | HTML | ✅ Ready | ~30 sec | ~350KB |

---

## 🚀 Features in Both Apps

- ✅ 44 tracked nutrients (macros, fats, vitamins, minerals)
- ✅ Barcode scanning
- ✅ Custom food creation
- ✅ Meal logging & history
- ✅ Daily/weekly goals
- ✅ Nutrition ring visualization
- ✅ localStorage persistence
- ✅ Responsive design (mobile + desktop)

---

## 📖 GitHub Actions

**View all builds:** https://github.com/san1eev1/calories-calculator/actions

**Workflow files:**
- `.github/workflows/build-android.yml`
- `.github/workflows/build-ios.yml`

Both workflows trigger automatically on push to the `claude/friendly-davinci-kz02xp` branch.
