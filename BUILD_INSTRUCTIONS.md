# Build Instructions for Tiffin Nutrition Tracker

This guide covers building Tiffin as a web app, iOS app, or Android app.

## Prerequisites

### For Web
- Python 3.6+ (for build.py)
- A modern web browser

### For Android
- Node.js 16+ and npm
- Android Studio (download from https://developer.android.com/studio)
- Android SDK (installed via Android Studio)
- Java Development Kit (JDK) 11+

### For iOS
- macOS 12+
- Xcode 14+ (download from App Store)
- CocoaPods (install with: `sudo gem install cocoapods`)
- Node.js 16+ and npm

## Building the Web App

```bash
# Build the single-file HTML app
npm run build:web

# The app is now available at dist/index.html
# Open it in any modern web browser
```

The web app is completely self-contained in a single HTML file with no external dependencies.

## Building for Android

### Setup (first time only)

1. **Install Android Studio** from https://developer.android.com/studio
2. **Open Android Studio** and install:
   - Android SDK (API level 30+)
   - Android emulator (or connect a physical device)
3. **Set up environment variables**:
   ```bash
   export ANDROID_HOME=~/Android/Sdk
   export PATH=$PATH:$ANDROID_HOME/tools:$ANDROID_HOME/tools/bin:$ANDROID_HOME/platform-tools
   ```

### Build APK

```bash
# Build and open Android Studio
npm run build:android

# In Android Studio:
# 1. Wait for Gradle sync to complete
# 2. Go to Build > Build Bundle(s) / APK(s) > Build APKs
# 3. Select "release" build type for production
# 4. The APK will be generated at: android/app/build/outputs/apk/

# To build without opening Android Studio:
cd android
./gradlew build
./gradlew assembleRelease  # For release APK

# Generated APK will be at:
# android/app/build/outputs/apk/release/app-release.apk
```

### Install on Device

```bash
# Connect an Android device via USB or launch an emulator

# Find connected devices
adb devices

# Install APK
adb install android/app/build/outputs/apk/release/app-release.apk

# Or if using Android Studio, click "Run" to install on connected device
```

## Building for iOS

### Setup (first time only)

1. **Install Xcode** from Mac App Store
2. **Install CocoaPods**:
   ```bash
   sudo gem install cocoapods
   ```
3. **Set up signing credentials** in Xcode for your Apple Developer Account

### Build IPA

```bash
# Build and open Xcode
npm run build:ios

# In Xcode:
# 1. Select your target device or simulator
# 2. Click Product > Build for > Running (to test in simulator)
# 3. Or click Product > Archive (to build for App Store)

# To build from command line:
cd ios/App
xcodebuild -workspace App.xcworkspace -scheme App -configuration Release -archivePath ../build archive
xcodebuild -exportArchive -archivePath ../build.xcarchive -exportOptionsPlist ../exportOptions.plist -exportPath ../build/ipa
```

### Install on Device

**Simulator:**
```bash
cd ios/App
xcodebuild -workspace App.xcworkspace -scheme App -configuration Debug -destination 'platform=iOS Simulator,name=iPhone 15'
```

**Physical Device:**
1. Connect your iPhone via USB
2. In Xcode: Select your device as the target
3. Click Product > Run
4. Trust the developer certificate on your phone (Settings > General > Device Management)

## Publishing to App Stores

### Google Play Store

1. Create a Google Play Developer account ($25 one-time fee)
2. Generate a signed release APK:
   ```bash
   cd android
   keytool -genkey -v -keystore release-key.keystore -alias tiffin -keyalg RSA -keysize 2048 -validity 10000
   ./gradlew assembleRelease -Pandroid.injected.signing.store.file=$(pwd)/release-key.keystore
   ```
3. Upload to Google Play Console
4. Fill in app details (description, screenshots, privacy policy, etc.)
5. Submit for review

### Apple App Store

1. Create an Apple Developer account ($99/year)
2. In Xcode, sign in with your Apple ID
3. Create an App ID and provisioning profiles
4. Build and archive:
   ```bash
   cd ios/App
   xcodebuild -workspace App.xcworkspace -scheme App -configuration Release archive
   ```
5. Upload to App Store Connect using Xcode or Transporter
6. Fill in app details and submit for review

## Development Workflow

### Making Changes

1. Edit `app.js`, `app.css`, or other source files
2. Run `npm run build` to rebuild
3. Changes will be reflected in `dist/index.html`
4. For mobile apps: Run `npm run build:android` or `npm run build:ios` to sync changes

### Testing on Devices

```bash
# Web
npm run build:web
# Open dist/index.html in browser

# Android
npm run build:android
# Then use Android Studio to run on emulator or connected device

# iOS
npm run build:ios
# Then use Xcode to run on simulator or connected device
```

## Troubleshooting

### Android issues
- **"Android SDK not found"**: Set `ANDROID_HOME` environment variable
- **Gradle build fails**: Try `./gradlew clean` then rebuild
- **APK won't install**: Ensure minimum API level is 30+

### iOS issues
- **"Pod install failed"**: Run `cd ios/App && pod repo update && pod install`
- **Code signing errors**: Check Apple Developer Team in Xcode (Signing & Capabilities tab)
- **Simulator won't launch**: Try `xcrun simctl erase all` to reset all simulators

### Web issues
- **Build fails**: Ensure Python 3.6+ is installed
- **App won't load**: Check browser console for errors, ensure `dist/index.html` exists

## Additional Resources

- [Capacitor Docs](https://capacitorjs.com)
- [Android Development](https://developer.android.com/develop)
- [iOS Development](https://developer.apple.com/develop)
- [App Store Submission Guide](https://developer.apple.com/app-store/review/guidelines/)

---

For support or questions, see the project repository or submit an issue.
