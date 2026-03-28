#!/bin/bash
# Build iOS app using Kotlin Multiplatform
# Run this script on macOS with Xcode 15+ installed

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🍎 Building CPA Songs iOS App (KMP)${NC}"
echo ""

# Check we're on macOS
if [[ "$(uname)" != "Darwin" ]]; then
    echo -e "${RED}❌ Error: This script must run on macOS${NC}"
    echo "iOS builds require macOS with Xcode installed"
    exit 1
fi

# Check Xcode is installed
if ! command -v xcodebuild &> /dev/null; then
    echo -e "${RED}❌ Error: Xcode not found${NC}"
    echo "Install Xcode from the Mac App Store"
    exit 1
fi

# Check Java is available
if ! command -v java &> /dev/null; then
    echo -e "${RED}❌ Error: Java not found${NC}"
    echo "Install JDK 17: brew install openjdk@17"
    exit 1
fi

echo -e "${YELLOW}📋 Environment:${NC}"
echo "  macOS: $(sw_vers -productVersion)"
echo "  Xcode: $(xcodebuild -version | head -n 1)"
echo "  Java: $(java -version 2>&1 | head -n 1)"
echo ""

# Navigate to project root
cd "$(dirname "$0")/.."
PROJECT_ROOT=$(pwd)
echo -e "${YELLOW}📁 Project: ${NC}$PROJECT_ROOT"
echo ""

# Build type: simulator (default) or device
BUILD_TYPE=${1:-simulator}

if [ "$BUILD_TYPE" == "simulator" ]; then
    echo -e "${GREEN}🔨 Building for iOS Simulator...${NC}"
    FRAMEWORK_TARGET="linkDebugFrameworkIosSimulatorArm64"
    SDK="iphonesimulator"
    DESTINATION="platform=iOS Simulator,name=iPhone 15 Pro"
    CONFIG="Debug"
elif [ "$BUILD_TYPE" == "device" ]; then
    echo -e "${GREEN}🔨 Building for iOS Device...${NC}"
    FRAMEWORK_TARGET="linkReleaseFrameworkIosArm64"
    SDK="iphoneos"
    DESTINATION="generic/platform=iOS"
    CONFIG="Release"
else
    echo -e "${RED}❌ Error: Invalid build type '$BUILD_TYPE'${NC}"
    echo "Usage: $0 [simulator|device]"
    exit 1
fi

# Step 1: Build KMP Shared Framework
echo ""
echo -e "${YELLOW}Step 1/3: Building KMP Shared Framework...${NC}"
./gradlew :shared:$FRAMEWORK_TARGET --no-daemon --stacktrace

# Verify framework was built
if [ "$BUILD_TYPE" == "simulator" ]; then
    FRAMEWORK_PATH="shared/build/bin/iosSimulatorArm64/debugFramework/shared.framework"
else
    FRAMEWORK_PATH="shared/build/bin/iosArm64/releaseFramework/shared.framework"
fi

if [ -d "$FRAMEWORK_PATH" ]; then
    echo -e "${GREEN}✅ Framework built: $FRAMEWORK_PATH${NC}"
    echo "   Size: $(du -sh $FRAMEWORK_PATH | cut -f1)"
else
    echo -e "${RED}❌ Framework not found at $FRAMEWORK_PATH${NC}"
    exit 1
fi

# Step 2: Copy Assets (if needed)
echo ""
echo -e "${YELLOW}Step 2/3: Checking iOS bundle assets...${NC}"

ASSETS_NEEDED=false

if [ ! -f "iosApp/iosApp/urdusongs.json" ]; then
    echo "  Copying urdusongs.json..."
    cp app/src/main/assets/urdusongs.json iosApp/iosApp/ 2>/dev/null || ASSETS_NEEDED=true
fi

if [ ! -f "iosApp/iosApp/englishsongs.json" ]; then
    echo "  Copying englishsongs.json..."
    cp app/src/main/assets/englishsongs.json iosApp/iosApp/ 2>/dev/null || ASSETS_NEEDED=true
fi

if [ ! -d "iosApp/iosApp/bible" ]; then
    echo "  Copying bible/ folder..."
    cp -r app/src/main/assets/bible iosApp/iosApp/ 2>/dev/null || ASSETS_NEEDED=true
fi

if [ "$ASSETS_NEEDED" == "true" ]; then
    echo -e "${YELLOW}⚠️  Warning: Some assets couldn't be copied${NC}"
    echo "   Make sure to add them to Xcode project manually:"
    echo "   1. Drag files into iosApp/iosApp in Xcode"
    echo "   2. Check 'Copy items if needed'"
    echo "   3. Ensure iosApp target is selected"
else
    echo -e "${GREEN}✅ Assets present${NC}"
fi

# Step 3: Build iOS App
echo ""
echo -e "${YELLOW}Step 3/3: Building iOS App with Xcode...${NC}"

cd iosApp

if [ "$BUILD_TYPE" == "device" ]; then
    # Device build (unsigned for testing)
    xcodebuild \
        -project iosApp.xcodeproj \
        -scheme iosApp \
        -configuration $CONFIG \
        -sdk $SDK \
        -destination "$DESTINATION" \
        -derivedDataPath ./build \
        clean build \
        CODE_SIGN_IDENTITY="" \
        CODE_SIGNING_REQUIRED=NO \
        CODE_SIGNING_ALLOWED=NO \
        | tee build.log | xcpretty || cat build.log

    # Create IPA
    echo ""
    echo -e "${YELLOW}Creating IPA...${NC}"
    cd build/Build/Products/Release-iphoneos
    mkdir -p Payload
    cp -r iosApp.app Payload/
    zip -r ../iosApp-unsigned.ipa Payload/
    cd "$PROJECT_ROOT"

    IPA_PATH="iosApp/build/Build/Products/iosApp-unsigned.ipa"
    if [ -f "$IPA_PATH" ]; then
        echo -e "${GREEN}✅ IPA created: $IPA_PATH${NC}"
        echo "   Size: $(du -sh $IPA_PATH | cut -f1)"
    fi
else
    # Simulator build
    xcodebuild \
        -project iosApp.xcodeproj \
        -scheme iosApp \
        -configuration $CONFIG \
        -sdk $SDK \
        -destination "$DESTINATION" \
        -derivedDataPath ./build \
        clean build \
        | tee build.log | xcpretty || cat build.log
fi

cd "$PROJECT_ROOT"

# Verify build output
if [ "$BUILD_TYPE" == "simulator" ]; then
    APP_PATH="iosApp/build/Build/Products/Debug-iphonesimulator/iosApp.app"
else
    APP_PATH="iosApp/build/Build/Products/Release-iphoneos/iosApp.app"
fi

echo ""
if [ -d "$APP_PATH" ]; then
    echo -e "${GREEN}✅ iOS App Built Successfully!${NC}"
    echo ""
    echo "   Location: $APP_PATH"
    echo "   Size: $(du -sh $APP_PATH | cut -f1)"
    echo ""

    if [ "$BUILD_TYPE" == "simulator" ]; then
        echo -e "${YELLOW}To run:${NC}"
        echo "   1. Open Simulator.app"
        echo "   2. Drag $APP_PATH onto the simulator"
        echo "   OR"
        echo "   3. Run in Xcode: cd iosApp && open iosApp.xcodeproj"
    else
        echo -e "${YELLOW}To install on device:${NC}"
        echo "   Use Xcode to deploy, or create signed IPA for TestFlight/App Store"
    fi
else
    echo -e "${RED}❌ iOS App Build Failed${NC}"
    echo "Check build.log in iosApp/ for details"
    exit 1
fi

echo ""
echo -e "${GREEN}🎉 Build complete!${NC}"

