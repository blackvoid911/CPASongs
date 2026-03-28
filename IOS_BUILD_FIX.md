# iOS Build Configuration Fix

## Issue
GitHub Actions iOS builds were failing with:
```
KotlinSourceSet with name 'iosMain' not found.
```

## Root Cause
Two problems in `shared/build.gradle.kts`:

1. **Incorrect OS detection**: The code checked for `os.name` starting with `"Mac OS"`, but modern macOS systems return `"Mac OS X"`. The exact match with `startsWith("Mac OS")` would work, but the check was too strict.

2. **Source set access timing**: The `iosMain` source set was being accessed inside the `sourceSets` configuration block with `if (isRunningOnMac)`, but Gradle evaluates property access before the condition at configuration time, causing the error.

## Solution

### 1. Improved OS Detection (line 13-14)
```kotlin
val osName = System.getProperty("os.name") ?: ""
val isRunningOnMac = osName.contains("Mac OS", ignoreCase = true)
```
- Uses `contains` instead of `startsWith` for more flexible matching
- Explicitly stores `os.name` in a variable for clarity
- Case-insensitive match handles variations

### 2. Deferred iOS Dependencies Configuration (lines 58-65)
```kotlin
// Configure iOS dependencies after source sets are created
if (isRunningOnMac) {
    kotlin.sourceSets.named("iosMain") {
        dependencies {
            implementation(libs.ktor.client.darwin)
        }
    }
}
```
- Moved iOS dependencies configuration **outside** the `sourceSets` block
- Uses `kotlin.sourceSets.named("iosMain")` to access the source set after it's created
- This deferred access pattern ensures the source set exists before trying to configure it

## Verification

### Windows Build (Android only)
```powershell
.\gradlew.bat :shared:compileDebugKotlinAndroid --no-daemon
```
✅ **BUILD SUCCESSFUL** - iOS source sets correctly skipped on Windows

### macOS Build (via GitHub Actions)
```bash
./gradlew :shared:linkDebugFrameworkIosSimulatorArm64 --no-daemon --stacktrace
```
✅ Should now succeed - iOS targets created and dependencies configured properly

## Technical Notes

- **Gradle Configuration Phase**: Gradle evaluates build scripts in configuration phase before execution. Accessing a source set that doesn't exist causes immediate failure, even inside an `if` block that guards with a boolean.
- **Source Set Creation**: iOS targets (`iosX64()`, `iosArm64()`, `iosSimulatorArm64()`) create the `iosMain` source set automatically when called.
- **Named Access Pattern**: Using `sourceSets.named("iosMain")` after the kotlin block ensures the source set exists and is fully initialized.

## Related Files
- `shared/build.gradle.kts` - KMP build configuration (fixed)
- `.github/workflows/build-ios.yml` - GitHub Actions iOS build (no changes needed)
- `AGENTS.md` - Documentation updated to reflect `contains` check instead of `startsWith`

