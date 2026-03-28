# GitHub Actions: Automated iOS Builds with KMP

## 🤖 Build iOS on Every Push (No Mac Required!)

GitHub Actions provides **free macOS runners** that can build your iOS app automatically using Kotlin Multiplatform.

---

## ✅ Setup Complete

I've created two GitHub Actions workflows:

### 1. `build-multiplatform.yml` (Both Platforms)
**Triggers**: Push to main/develop, pull requests, manual
**Builds**:
- ✅ Android debug APK
- ✅ Android release AAB (if keystore exists)
- ✅ iOS simulator app (debug)
- ✅ iOS device build (release, main branch only)

**Runtime**: ~10-15 minutes total

### 2. `build-ios.yml` (iOS Only)
**Triggers**: Push to main/develop (if iOS code changes), manual
**Builds**:
- ✅ iOS simulator (debug)
- ✅ iOS device (release, unsigned)

**Runtime**: ~5-8 minutes

---

## 🚀 How to Use

### First Time Setup:

1. **Push workflows to GitHub**:
   ```bash
   cd C:\Users\WelCome\AndroidStudioProjects\CPASongs
   git add .github/workflows/
   git commit -m "Add GitHub Actions for iOS/Android KMP builds"
   git push
   ```

2. **Workflows run automatically**:
   - On every push to main/develop
   - On every pull request
   - Or manually via GitHub Actions tab

### View Build Status:

1. Go to your GitHub repo
2. Click **Actions** tab
3. See builds in progress / completed
4. Download artifacts (APK, AAB, iOS .app)

### Manual Trigger:

1. Go to **Actions** tab
2. Select workflow (e.g., "Build iOS (KMP Framework)")
3. Click **Run workflow**
4. Select branch
5. Click **Run workflow** button

---

## 📦 Artifacts Downloaded Automatically

After each build, artifacts are uploaded:

| Artifact Name | Platform | Type | Retention |
|---------------|----------|------|-----------|
| `android-debug-apk` | Android | APK | 14 days |
| `android-release-aab` | Android | AAB | 30 days |
| `ios-simulator-debug` | iOS | .app | 14 days |
| `ios-device-unsigned-ipa` | iOS | IPA | 30 days |

### Download Artifacts:

1. Go to **Actions** tab
2. Click on a completed workflow run
3. Scroll to **Artifacts** section
4. Click artifact name to download ZIP

---

## 🔐 Signing Configuration (Optional)

### Android Signing (Already Configured)
The keystore is checked into the repo:
```
app/cpasongs-release-key.keystore
```

GitHub Actions will automatically sign Android AABs.

### iOS Signing (For App Store Upload)

To enable signed iOS builds, add secrets to GitHub:

1. Go to repo → **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Add these secrets:

| Secret Name | Value | Purpose |
|-------------|-------|---------|
| `IOS_CERTIFICATE_BASE64` | Base64-encoded .p12 cert | Code signing |
| `IOS_CERTIFICATE_PASSWORD` | Password for .p12 | Unlock cert |
| `IOS_PROVISIONING_PROFILE_BASE64` | Base64-encoded .mobileprovision | App Store profile |
| `APPLE_ID` | Your Apple ID email | Upload to App Store |
| `APPLE_APP_SPECIFIC_PASSWORD` | App-specific password | Authentication |

### How to Get Certificates:

**Export from Xcode**:
```bash
# On a Mac with signing set up:
# 1. Open Keychain Access
# 2. Find "Apple Distribution: Your Name"
# 3. Right-click → Export "Apple Distribution..."
# 4. Save as .p12 with password

# Convert to base64:
base64 -i YourCertificate.p12 | pbcopy
# Paste into GitHub secret IOS_CERTIFICATE_BASE64

# Export provisioning profile:
cd ~/Library/MobileDevice/Provisioning\ Profiles/
# Find your profile (UUID.mobileprovision)
base64 -i YourProfile.mobileprovision | pbcopy
# Paste into GitHub secret IOS_PROVISIONING_PROFILE_BASE64
```

---

## 📊 Workflow Details

### Build Matrix (Optional)

You can modify workflows to build multiple iOS variants:

```yaml
strategy:
  matrix:
    ios-destination:
      - 'platform=iOS Simulator,name=iPhone 15 Pro'
      - 'platform=iOS Simulator,name=iPhone 15'
      - 'platform=iOS Simulator,name=iPad Pro 12.9-inch'
```

### Caching

Workflows cache:
- ✅ Gradle dependencies (`~/.gradle/caches`)
- ✅ KMP Konan dependencies (`~/.konan`)
- ✅ KMP built frameworks (`shared/build/bin`)

**First build**: ~10-15 minutes  
**Cached builds**: ~3-5 minutes

---

## 🧪 Testing on GitHub Actions

### View Logs:

1. Click workflow run
2. Expand job (e.g., "Build iOS (KMP)")
3. Click step (e.g., "Build KMP Shared Framework")
4. See full terminal output

### Debug Failed Builds:

Look for errors in these steps:
- **Build KMP Shared Framework**: Kotlin compilation errors
- **Build iOS App**: Swift/Xcode errors
- **Verify Framework Built**: Framework not generated

Common issues:
- **Gradle timeout**: Increase `--no-daemon` timeout
- **Xcode scheme not found**: Check scheme name in `.xcodeproj`
- **Framework not linked**: Verify output path in build script

---

## 🎯 Workflow Triggers

### Automatic Triggers:

**Push to main/develop**:
```yaml
on:
  push:
    branches: [ main, develop ]
```

**Pull Requests**:
```yaml
on:
  pull_request:
    branches: [ main ]
```

**Path filters** (iOS workflow only):
```yaml
on:
  push:
    paths:
      - 'shared/**'      # KMP shared code
      - 'iosApp/**'      # iOS-specific code
      - '.github/workflows/build-ios.yml'
```

**Manual trigger**:
```yaml
on:
  workflow_dispatch:  # Adds "Run workflow" button
```

---

## 📱 Running iOS Builds Locally (macOS)

If you have a Mac, you can test the workflow steps locally:

```bash
# Clone repo on Mac
git clone https://github.com/YOUR_USERNAME/CPASongs.git
cd CPASongs

# Run the build script
chmod +x build-ios.sh
./build-ios.sh simulator  # For simulator
./build-ios.sh device     # For device
```

Or use Xcode:
```bash
cd iosApp
open iosApp.xcodeproj
# Press ⌘ + R
```

---

## 🔄 CI/CD Pipeline

### Full Pipeline (Recommended):

```
1. Developer pushes to develop branch
     ↓
2. GitHub Actions builds Android + iOS
     ↓
3. If tests pass, merge to main
     ↓
4. GitHub Actions builds release versions
     ↓
5. Download signed AAB/IPA artifacts
     ↓
6. Upload to Play Store / App Store Connect
```

### Release Workflow (Add Later):

You can extend workflows to automatically upload to stores:

```yaml
- name: Upload to App Store Connect
  env:
    APPLE_ID: ${{ secrets.APPLE_ID }}
    APPLE_PASSWORD: ${{ secrets.APPLE_APP_SPECIFIC_PASSWORD }}
  run: |
    xcrun altool --upload-app \
      --type ios \
      --file iosApp.ipa \
      --username $APPLE_ID \
      --password $APPLE_PASSWORD
```

---

## 📊 Monitoring Builds

### Build Status Badge

Add to README.md:
```markdown
![Android Build](https://github.com/YOUR_USERNAME/CPASongs/actions/workflows/build-multiplatform.yml/badge.svg)
![iOS Build](https://github.com/YOUR_USERNAME/CPASongs/actions/workflows/build-ios.yml/badge.svg)
```

### Email Notifications

GitHub sends emails for:
- ✅ Build success
- ❌ Build failure
- Configure in repo Settings → Notifications

### Slack/Discord Integration

Add webhook to workflows:
```yaml
- name: Notify Slack
  if: always()
  uses: 8398a7/action-slack@v3
  with:
    status: ${{ job.status }}
    webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

---

## 💰 Cost (FREE!)

GitHub Actions provides **free minutes** for public repos:
- ✅ Unlimited for public repositories
- ✅ 2,000 minutes/month for private repos (Free tier)
- ✅ macOS runners count as 10x (so ~200 builds/month on free tier)

**For private repos with heavy usage**: Upgrade to Team ($4/user/month) or Enterprise.

---

## 🔧 Advanced Configuration

### Matrix Builds (Multiple Targets):

```yaml
strategy:
  matrix:
    target:
      - iosSimulatorArm64      # M1/M2/M3 Macs
      - iosX64                 # Intel Macs
      - iosArm64               # Physical devices
```

### Conditional Steps:

```yaml
- name: Upload to TestFlight
  if: github.ref == 'refs/heads/main' && success()
  run: ./upload-testflight.sh
```

### Scheduled Builds (Nightly):

```yaml
on:
  schedule:
    - cron: '0 2 * * *'  # 2 AM UTC daily
```

---

## 🆘 Troubleshooting

### "Framework not found"
**Cause**: Gradle task failed silently  
**Fix**: Check `linkDebugFrameworkIosSimulatorArm64` logs

### "Xcode build failed"
**Cause**: Swift compilation error or missing assets  
**Fix**: Check ContentView.swift, ensure assets are in bundle

### "Timeout after 360 minutes"
**Cause**: Build hung (rare)  
**Fix**: Add `timeout-minutes: 30` to job

### "Out of disk space"
**Cause**: Large derived data  
**Fix**: Add cleanup step:
```yaml
- name: Clean up
  run: rm -rf ~/Library/Developer/Xcode/DerivedData
```

---

## 📝 Next Steps

### After First Successful Build:

1. **Download iOS Simulator .app** from artifacts
2. **Test on local Mac** by dragging to simulator
3. **Verify all features work**:
   - Song loading (API sync)
   - Bible reader
   - Search (songs + Bible)
   - Urdu RTL rendering
   - Navigation

### For App Store Distribution:

1. **Add signing secrets** (see section above)
2. **Modify workflow** to sign builds
3. **Upload to TestFlight** automatically
4. **Distribute to testers**

### For Continuous Deployment:

Create `deploy.yml` workflow:
```yaml
on:
  release:
    types: [published]

jobs:
  deploy:
    runs-on: macos-14
    steps:
      - # Build signed iOS
      - # Upload to App Store Connect
      - # Upload Android to Play Console
```

---

## 🎯 Benefits of GitHub Actions KMP Builds

✅ **No Mac Required**: Builds run on GitHub's macOS runners  
✅ **Automatic**: Builds on every push  
✅ **Fast**: Cached dependencies speed up builds  
✅ **Artifacts**: Download builds directly  
✅ **Free**: Unlimited for public repos  
✅ **Reliable**: Consistent build environment  
✅ **Shareable**: Team members can download builds  

---

## 🚀 Activation

To activate GitHub Actions:

```bash
# From Windows, push the workflows:
cd C:\Users\WelCome\AndroidStudioProjects\CPASongs

git add .github/
git add build-ios.sh
git add iosApp/README.md
git add iosApp/ExportOptions.plist

git commit -m "Add GitHub Actions for KMP iOS/Android builds"
git push origin main
```

Then:
1. Go to GitHub repo → **Actions** tab
2. You'll see workflows running automatically
3. Wait ~10-15 minutes for first build
4. Download artifacts when complete

**Your iOS app will be built on macOS in the cloud!** 🎉

---

## Summary

✅ **GitHub Actions workflows created** (2 files)  
✅ **iOS build script created** (build-ios.sh)  
✅ **iOS README created** (iosApp/README.md)  
✅ **Export options created** (ExportOptions.plist)  

**Next**: Push to GitHub and watch the magic happen! 🪄

The workflows will:
1. Build KMP shared framework on macOS runner
2. Build iOS app with Xcode
3. Upload artifacts for download
4. All automatically, no Mac required locally!

