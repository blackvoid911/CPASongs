# CPA Songs - iOS App

## Kotlin Multiplatform iOS App

This iOS app is built using **Kotlin Multiplatform (KMP)** and **Compose Multiplatform**, sharing 100% of the UI code with the Android app.

---

## Architecture

### Shared Code (from `:shared` module)
- **UI**: All screens, navigation, components
- **Business Logic**: Song loading, Bible parsing, search
- **Data Models**: SongItem, BibleBook, etc.
- **Networking**: Ktor HttpClient (Darwin engine on iOS)
- **Serialization**: kotlinx.serialization

### iOS-Specific Code
- **Platform.ios.kt**: File I/O via NSBundle/NSDocumentDirectory, NSUserDefaults, time
- **MainViewController.kt**: Compose entry point
- **ContentView.swift**: UIViewControllerRepresentable bridge
- **iOSApp.swift**: SwiftUI app entry point

---

## Building on macOS

### Prerequisites:
- macOS 13+ (Ventura or later)
- Xcode 15.0+
- JDK 17 (for Gradle/KMP)

### Quick Start:

```bash
# 1. Open in Xcode
cd iosApp
open iosApp.xcodeproj

# 2. Select target: "iosApp" scheme, iPhone simulator or device

# 3. Build and Run (⌘ + R)
```

The Xcode build script automatically:
1. Runs Gradle to build the KMP shared framework
2. Links the framework to the Swift app
3. Compiles and runs

### Terminal Build:

```bash
# Build Simulator app
cd iosApp
xcodebuild \
  -project iosApp.xcodeproj \
  -scheme iosApp \
  -sdk iphonesimulator \
  -destination 'platform=iOS Simulator,name=iPhone 15 Pro' \
  build
```

---

## Configuration

### Bundle Identifier
`com.cpa.cpasongs.ios`

### Deployment Target
iOS 15.0+ (required for Compose Multiplatform)

### App Version
- **Version**: 1.0.4
- **Build Number**: 5

Update in Xcode:
1. Select project → iosApp target → General
2. Update "Version" and "Build"

---

## Required Assets

### 1. Copy Song & Bible JSON Files

**From**:
```
../app/src/main/assets/
  ├── urdusongs.json
  ├── englishsongs.json
  └── bible/
      ├── genesis.json ... revelation.json (66 books)
      └── urdu/
          └── genesis.json ... revelation.json (66 books)
```

**To**:
```
iosApp/
  ├── urdusongs.json
  ├── englishsongs.json
  └── bible/
      └── (all JSON files)
```

**Then in Xcode**:
1. Drag files/folders into `iosApp` group
2. Check "Copy items if needed"
3. Ensure "iosApp" target is checked
4. Verify they appear in "Build Phases → Copy Bundle Resources"

### 2. Add Urdu Font (Optional but Recommended)

**Download**:
- Get `NotoNastaliqUrdu-Regular.ttf` from [Google Fonts](https://fonts.google.com/noto/specimen/Noto+Nastaliq+Urdu)

**Add to Xcode**:
1. Drag TTF into `iosApp` group
2. Check "Copy items if needed"
3. Target: iosApp

**Register in Info.plist**:
```xml
<key>UIAppFonts</key>
<array>
    <string>NotoNastaliqUrdu-Regular.ttf</string>
</array>
```

**Update Platform.ios.kt**:
```kotlin
@Composable
actual fun urduFontFamily(): FontFamily = 
    FontFamily(Font("NotoNastaliqUrdu-Regular"))
```

### 3. Replace App Icon

1. Open `Assets.xcassets` in Xcode
2. Select `AppIcon`
3. Drag 1024×1024 PNG into "App Store iOS 1024pt" slot
4. Xcode generates all required sizes

---

## Features

All features from the Android app work identically:

- ✅ **Song Book**: Urdu + English songs with categories (Geet, Zaboor)
- ✅ **Bible Reader**: KJV English + Urdu translation (66 books each)
- ✅ **API Sync**: Automatic song updates from CPA-PK.org
- ✅ **Search**: Full-text search in songs and Bible
- ✅ **Offline Mode**: Works without internet after first sync
- ✅ **RTL Support**: Proper Urdu text rendering
- ✅ **Material 3 Design**: Modern UI with animations
- ✅ **Dark Mode**: Automatic theme switching

---

## Development Notes

### KMP Framework Build

The shared framework is built by Gradle:

```bash
# Debug (Simulator)
./gradlew :shared:linkDebugFrameworkIosSimulatorArm64

# Release (Device)
./gradlew :shared:linkReleaseFrameworkIosArm64

# Output:
shared/build/bin/iosSimulatorArm64/debugFramework/shared.framework
shared/build/bin/iosArm64/releaseFramework/shared.framework
```

### Xcode Build Script

Found in project → Build Phases → "Build KMP Shared Framework":
```bash
cd "${SRCROOT}/.."
if [ "${CONFIGURATION}" == "Debug" ]; then
  ./gradlew :shared:linkDebugFrameworkIosSimulatorArm64
else
  ./gradlew :shared:linkReleaseFrameworkIosArm64
fi
```

### Clean Build

If you encounter caching issues:

```bash
# Clean Gradle
./gradlew clean

# Clean Xcode
cd iosApp
xcodebuild clean -project iosApp.xcodeproj -scheme iosApp

# Clean derived data
rm -rf ~/Library/Developer/Xcode/DerivedData
```

---

## App Store Submission

### 1. Create Archive:

```bash
cd iosApp

xcodebuild archive \
  -project iosApp.xcodeproj \
  -scheme iosApp \
  -configuration Release \
  -archivePath ./build/iosApp.xcarchive
```

### 2. Export IPA:

```bash
xcodebuild \
  -exportArchive \
  -archivePath ./build/iosApp.xcarchive \
  -exportPath ./build \
  -exportOptionsPlist ExportOptions.plist
```

**Note**: Update `ExportOptions.plist` with your Team ID first!

### 3. Upload:

**Option A**: Xcode Organizer (GUI)
- Window → Organizer → Archives
- Select archive → Distribute App
- Follow wizard

**Option B**: Terminal (requires Apple ID credentials)
```bash
xcrun altool --upload-app \
  --type ios \
  --file build/iosApp.ipa \
  --username YOUR_APPLE_ID \
  --password YOUR_APP_SPECIFIC_PASSWORD
```

---

## Troubleshooting

### Framework not found in Xcode
**Solution**: Build framework manually first
```bash
./gradlew :shared:linkDebugFrameworkIosSimulatorArm64
```

### Swift cannot find MainViewControllerKt
**Solution**: 
1. Clean build folder (Shift + ⌘ + K)
2. Rebuild framework
3. Build iOS app again

### Assets not found at runtime
**Solution**: Verify in Xcode Build Phases → Copy Bundle Resources

### Signing errors
**Solution**: 
1. Select project → iosApp target → Signing & Capabilities
2. Select your Team
3. Enable "Automatically manage signing"

---

## Testing

### On Simulator:
```bash
# Build and install
xcodebuild \
  -project iosApp.xcodeproj \
  -scheme iosApp \
  -sdk iphonesimulator \
  -destination 'platform=iOS Simulator,name=iPhone 15 Pro' \
  build

# Launch simulator
open -a Simulator
```

### On Device:
1. Connect iPhone/iPad via USB
2. Select device in Xcode
3. Click Run (⌘ + R)
4. Trust certificate on device if prompted

---

## Version Management

Keep versions in sync with Android:

| Android | iOS |
|---------|-----|
| `versionName = "1.0.4"` | `CFBundleShortVersionString = "1.0.4"` |
| `versionCode = 5` | `CFBundleVersion = "5"` |

Update in Xcode or edit `project.pbxproj` directly.

---

## CI/CD

GitHub Actions workflows are set up in `.github/workflows/`:
- `build-multiplatform.yml` — Builds both Android + iOS
- `build-ios.yml` — iOS-only build

Triggers on push to main/develop branches.

Artifacts uploaded:
- `ios-simulator-debug` — For testing
- `ios-device-unsigned-ipa` — For ad-hoc distribution

---

## Support

For KMP-specific issues:
- Check [Kotlin Multiplatform docs](https://kotlinlang.org/docs/multiplatform.html)
- Check [Compose Multiplatform docs](https://www.jetbrains.com/lp/compose-multiplatform/)

For iOS-specific issues:
- Check `shared/src/iosMain/kotlin/` for platform code
- Check Xcode console for runtime errors
- Use Console.app to view logs: `[CPA_SONGS]` tag

---

## Current Status

✅ **KMP Configuration**: Complete
✅ **iOS Code**: Complete  
✅ **Xcode Project**: Configured  
✅ **Build Scripts**: Ready  
⏳ **Build**: Requires macOS + Xcode  

**To build**: Run on a Mac or use GitHub Actions!

