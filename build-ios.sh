#!/bin/bash
set -e

echo "🍎 Tiffin iOS App Builder"
echo "========================="
echo ""

# Check if running on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "❌ This script only works on macOS"
    echo "For Linux/Windows, use GitHub Actions to build:"
    echo "https://github.com/san1eev1/calories-calculator/actions"
    exit 1
fi

# Check prerequisites
echo "📋 Checking prerequisites..."

if ! command -v node &> /dev/null; then
    echo "❌ Node.js not found. Install from: https://nodejs.org"
    exit 1
fi

if ! command -v xcode-select &> /dev/null; then
    echo "❌ Xcode not found. Install from App Store:"
    echo "https://apps.apple.com/app/xcode/id497799835"
    exit 1
fi

if ! command -v pod &> /dev/null; then
    echo "⚠️  CocoaPods not found. Installing..."
    sudo gem install cocoapods
fi

echo "✅ All prerequisites found"
echo ""

# Build steps
echo "📦 Building iOS app..."
echo ""

echo "1️⃣  Installing npm dependencies..."
npm install

echo ""
echo "2️⃣  Building web app..."
npm run build

echo ""
echo "3️⃣  Syncing to iOS..."
npx cap sync ios

echo ""
echo "4️⃣  Installing CocoaPods..."
cd ios/App
pod install --repo-update
cd ../..

echo ""
echo "5️⃣  Building with Xcode..."
cd ios/App
xcodebuild build-for-testing \
    -workspace App.xcworkspace \
    -scheme App \
    -configuration Release \
    -derivedDataPath build

BUILD_APP="build/Build/Products/Release-iphoneos/App.app"

if [ -d "$BUILD_APP" ]; then
    echo ""
    echo "✅ SUCCESS!"
    echo ""
    echo "📱 Your iOS app is ready at:"
    echo "   $PWD/$BUILD_APP"
    echo ""
    echo "📲 Next steps:"
    echo ""
    echo "Option A - Install on iPhone (via Xcode):"
    echo "  1. Connect your iPhone via USB"
    echo "  2. Open Xcode: open App.xcworkspace"
    echo "  3. Select your iPhone from device selector"
    echo "  4. Click Product → Run"
    echo ""
    echo "Option B - Install on iPhone (via command line):"
    echo "  xcodebuild -scheme App -destination 'platform=iOS,name=YOUR_DEVICE_NAME' install"
    echo ""
    echo "Option C - Create IPA for App Store:"
    echo "  xcodebuild -exportArchive \\"
    echo "    -archivePath build/App.xcarchive \\"
    echo "    -exportOptionsPlist ExportOptions.plist \\"
    echo "    -exportPath build/ipa"
    echo ""
else
    echo ""
    echo "❌ Build failed. Check errors above."
    exit 1
fi
