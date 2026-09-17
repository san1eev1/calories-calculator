#!/bin/bash
set -e

echo "🤖 Tiffin Android App Builder"
echo "============================="
echo ""

# Check if on Linux or macOS with Android SDK
if [ -z "$ANDROID_HOME" ]; then
    if [ -d "$HOME/Android/Sdk" ]; then
        export ANDROID_HOME="$HOME/Android/Sdk"
    elif [ -d "$HOME/Library/Android/sdk" ]; then
        export ANDROID_HOME="$HOME/Library/Android/sdk"
    else
        echo "❌ Android SDK not found."
        echo "Install Android Studio from: https://developer.android.com/studio"
        exit 1
    fi
fi

export PATH=$PATH:$ANDROID_HOME/tools:$ANDROID_HOME/tools/bin:$ANDROID_HOME/platform-tools

echo "📋 Checking prerequisites..."

if ! command -v node &> /dev/null; then
    echo "❌ Node.js not found. Install from: https://nodejs.org"
    exit 1
fi

if ! command -v java &> /dev/null; then
    echo "❌ Java not found. Install Java 11+"
    exit 1
fi

if [ ! -d "$ANDROID_HOME" ]; then
    echo "❌ Android SDK not found at: $ANDROID_HOME"
    exit 1
fi

echo "✅ All prerequisites found"
echo ""

# Build steps
echo "📦 Building Android app..."
echo ""

echo "1️⃣  Installing npm dependencies..."
npm install

echo ""
echo "2️⃣  Building web app..."
npm run build

echo ""
echo "3️⃣  Syncing to Android..."
npx cap sync android

echo ""
echo "4️⃣  Building Android APK..."
cd android
chmod +x gradlew
./gradlew assembleRelease

APK_PATH="app/build/outputs/apk/release/app-release.apk"

if [ -f "$APK_PATH" ]; then
    echo ""
    echo "✅ SUCCESS!"
    echo ""
    echo "📱 Your Android APK is ready at:"
    echo "   $PWD/$APK_PATH"
    echo ""
    echo "📲 Next steps:"
    echo ""
    echo "Option A - Install on Android phone (via adb):"
    echo "  1. Connect your phone via USB (enable USB debugging)"
    echo "  2. Run: adb install $APK_PATH"
    echo ""
    echo "Option B - Upload to Google Play Store:"
    echo "  1. Go to https://play.google.com/console"
    echo "  2. Create a new app"
    echo "  3. Upload the APK"
    echo "  4. Fill in app details and screenshots"
    echo "  5. Submit for review"
    echo ""
else
    echo ""
    echo "❌ Build failed. Check errors above."
    exit 1
fi
