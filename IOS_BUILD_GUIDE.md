# iOS App Build Guide

This guide walks you through building the Tiffin iOS app on your Mac.

## Prerequisites

- **macOS 12 or later** (Monterey, Ventura, or Sonoma)
- **Xcode 14 or later** (download from [App Store](https://apps.apple.com/app/xcode/id497799835))
- **Xcode Command Line Tools**: After installing Xcode, run:
  ```bash
  xcode-select --install
  ```
- **Node.js 16+** (download from [nodejs.org](https://nodejs.org))
- **CocoaPods** (install with): 
  ```bash
  sudo gem install cocoapods
  ```
- **Apple Developer Account** (for signing and publishing)

## Quick Start - Build for Testing

### 1. Clone and Setup
```bash
git clone https://github.com/san1eev1/calories-calculator.git
cd calories-calculator
npm install
```

### 2. Build Web App
```bash
npm run build
```

### 3. Sync to iOS and Open Xcode
```bash
npm run build:ios
```
This opens Xcode automatically with the iOS project ready to build.

### 4. Select Simulator and Build
In Xcode:
1. Select **iPhone 15** (or your preferred simulator) from the top toolbar
2. Click **Product → Build** (or press ⌘B)
3. Once built, click **Product → Run** to launch the app in the simulator

## Building for Device Testing

### 1. Connect Your iPhone via USB
- Plug in your iPhone with a USB cable
- Trust this computer when prompted on your phone

### 2. Select Your Device
In Xcode, click on the device selector dropdown at the top and select your iPhone

### 3. Sign the App
In Xcode:
1. Click on **App** in the project navigator
2. Select the **App** target
3. Go to **Signing & Capabilities**
4. For **Team**, select your Apple Developer account
5. Xcode will automatically configure signing

### 4. Build and Run
```bash
cd ios/App
xcodebuild -workspace App.xcworkspace -scheme App -configuration Debug -destination 'platform=iOS,name=YOUR_DEVICE_NAME'
```

Or just click **Product → Run** in Xcode (easier)

### 5. Trust the Developer Certificate
On your iPhone:
1. Go to **Settings → General → Device Management**
2. Select your Apple ID
3. Tap **Trust**

## Building Release IPA for App Store

### 1. Create an App ID in Apple Developer
1. Go to [developer.apple.com](https://developer.apple.com)
2. Sign in with your Apple ID
3. Go to **Certificates, Identifiers & Profiles**
4. Click **Identifiers** → **+** to create new App ID
5. Use Bundle ID: `com.calories.tiffin`

### 2. Archive the App
In Xcode:
1. Select **Any iOS Device (arm64)** from the device selector
2. Click **Product → Archive**
3. Wait for the archive to complete

### 3. Export the IPA
When the archive completes:
1. The Organizer window opens
2. Select your archive
3. Click **Distribute App**
4. Choose **Apple App Store** (or **Ad Hoc** for testing)
5. Follow the signing prompts
6. Save the IPA file to your computer

## Manual Command-Line Build

### Build for iOS Simulator
```bash
cd ios/App
xcodebuild build-for-testing \
  -workspace App.xcworkspace \
  -scheme App \
  -configuration Release \
  -sdk iphonesimulator \
  -derivedDataPath build
```

### Build for Device
```bash
cd ios/App
xcodebuild archive \
  -workspace App.xcworkspace \
  -scheme App \
  -configuration Release \
  -archivePath build/App.xcarchive
```

### Export IPA
```bash
cd ios/App
xcodebuild -exportArchive \
  -archivePath build/App.xcarchive \
  -exportOptionsPlist ExportOptions.plist \
  -exportPath build/ipa
```

The IPA will be at: `build/ipa/App.ipa`

## Publishing to Apple App Store

### 1. Create App on App Store Connect
1. Go to [appstoreconnect.apple.com](https://appstoreconnect.apple.com)
2. Click **My Apps** → **+** to create a new app
3. Choose platform: **iOS**
4. Fill in app details:
   - **Name**: Tiffin
   - **Bundle ID**: com.calories.tiffin
   - **SKU**: any unique identifier
   - **Primary Language**: English

### 2. Fill in App Information
- **App Description**: "A self-contained nutrition tracker. Log meals, track macros and micronutrients, and achieve your health goals."
- **Keywords**: nutrition, fitness, calories, diary, tracker
- **Support URL**: Your support link
- **Privacy Policy URL**: Required for App Store

### 3. Add App Icons and Screenshots
- **App Icon**: 1024x1024 PNG (required)
- **Screenshots**: At least one screenshot for each device (iPhone, iPad)
  - iPhone: 1170×2532 or 1284×2778
  - iPad: 2048×2732

### 4. Set Pricing and Availability
- Choose pricing tier (e.g., Free)
- Select availability regions

### 5. Add Build and Submit for Review
1. Build and archive the app (see "Building Release IPA" above)
2. Upload using Xcode or Transporter:
   ```bash
   xcrun altool --upload-app \
     -f build/ipa/App.ipa \
     -t ios \
     -u your-apple-id@example.com \
     -p your-app-specific-password
   ```
3. Go to App Store Connect → Your App → Build
4. Select the uploaded build
5. Click **Submit for Review**
6. Review app details and submit

### 6. Wait for Apple Review
- Review typically takes 24-48 hours
- You'll receive an email when approved or if changes are needed

## Troubleshooting

### "Xcode not found"
```bash
sudo xcode-select --switch /Applications/Xcode.app/Contents/Developer
```

### "Pod install failed"
```bash
cd ios/App
pod repo update
pod install
```

### "Code signing error"
1. In Xcode: **App → Signing & Capabilities**
2. Check that a team is selected
3. Ensure you're using the correct provisioning profile

### "Cannot find CocoaPods"
```bash
sudo gem install cocoapods -v 1.14.0
pod repo update
cd ios/App
pod install
```

### "Simulator not working"
```bash
# Reset all simulators
xcrun simctl erase all

# Launch a fresh simulator
xcrun simctl create "iPhone 15" com.apple.CoreSimulator.SimDeviceType.iPhone-15 com.apple.CoreSimulator.SimRuntime.iOS-17-2
```

## Getting Help

- [Apple Developer Documentation](https://developer.apple.com/documentation/)
- [Capacitor iOS Guide](https://capacitorjs.com/docs/ios)
- [GitHub Issues](https://github.com/san1eev1/calories-calculator/issues)

---

## TL;DR - Fastest Path to App Store

```bash
# 1. Setup
git clone https://github.com/san1eev1/calories-calculator.git
cd calories-calculator
npm install

# 2. Build
npm run build
npm run build:ios

# 3. In Xcode (opens automatically):
#    - Select "Any iOS Device (arm64)"
#    - Product → Archive
#    - Distribute App → App Store
#    - Follow signing prompts

# 4. Upload to App Store Connect
#    - Upload in Xcode organizer
#    - Add screenshots and details
#    - Submit for Review

# Done! Your app goes to review in 24-48 hours
```
