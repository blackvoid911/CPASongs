# iOS Build Failure - Diagnostic & Fix

## Current Status

**Previous Build**: ❌ Failed with exit code 1
**Latest Fix Applied**: ✅ Removed NSUserDefaults.synchronize() (not available in K/N)
**Status**: ⏳ Awaiting next GitHub Actions build

---

## Potential Issues Fixed

### Issue #1: NSUserDefaults.synchronize() (FIXED)

**Problem**: K/N doesn't have the `synchronize()` method on NSUserDefaults

**Before**:
```kotlin
defaults.setObjectForKey(NSNumber(longLong = version), "songs_version")
defaults.synchronize()  // ❌ Not in K/N stdlib
```

**After**:
```kotlin
defaults.setObjectForKey(NSNumber(longLong = version), "songs_version")
// ✅ No synchronize() needed - K/N handles auto-sync
```

**Why**: K/N NSUserDefaults auto-syncs; calling synchronize() causes unresolved reference error

---

## Common iOS K/N Build Errors & Solutions

If the build still fails, check for these common issues:

### ❌ Error: "Unresolved reference 'XXX'"
- Check that the API exists in Kotlin/Native stdlib
- Many Objective-C APIs have different names in K/N
- Solution: Cast or use different API

### ❌ Error: "This declaration needs opt-in"
- Add `@OptIn(...)` annotation to the function using the API
- Solutions applied in this project:
  - `@OptIn(ExperimentalForeignApi::class)` for NSString.create()
  - `@OptIn(ExperimentalLayoutApi::class)` for CPAMainApp()

### ❌ Error: "Cannot access property on constructor"
- K/N doesn't allow chaining property access on constructor results
- Solution: Split into separate statements
- Example already fixed:
  ```kotlin
  val date = NSDate()
  val interval = date.timeIntervalSince1970
  return (interval * 1000).toLong()
  ```

### ❌ Error: "None of the following candidates is applicable"
- The specific constructor overload doesn't exist in K/N
- Solution: Find the correct typed constructor
- Example already fixed:
  ```kotlin
  NSNumber(longLong = version)  // Not NSNumber(value:)
  ```

---

## Files Currently Fixed

### 1. Platform.ios.kt
✅ Line 35: @OptIn for NSString.create() in readAssetFile()
✅ Line 45: @OptIn for NSString.create() in readCacheFile()
✅ Line 62: Changed numberForKey() → objectForKey()
✅ Line 67: Changed setObject() → setObjectForKey()
✅ Line 68: Changed NSNumber(value:) → NSNumber(longLong:)
✅ Line 77-80: Split NSDate().timeIntervalSince1970 into statements
✅ JUST NOW: Removed synchronize() call

### 2. CPAApp.kt
✅ Line 79: Added @OptIn(ExperimentalLayoutApi::class) to CPAMainApp()

---

## Next Build Triggers

GitHub Actions will automatically build when:
1. ✅ Commit pushed to master (just done)
2. ✅ Changes touch shared/ or iosApp/ (both affected)

**Check progress**: https://github.com/blackvoid911/CPASongs/actions

---

## If Build Still Fails

1. **Check GitHub Actions logs** for the specific error message
2. **Error patterns to look for**:
   - Unresolved reference → Add @OptIn or use different API
   - "This declaration needs opt-in" → Add @OptIn annotation
   - Type mismatch → Check constructor overloads
3. **Report the exact error line** and we'll fix it immediately

---

## Recent Commits

```
3de1f7d - Fix iOS K/N: remove NSUserDefaults.synchronize()
58f4bf7 - Add build status report
0e9f454 - Add iOS K/N fixes documentation
6e83332 - Fix iOS K/N compilation errors (main fixes)
```

---

**Last Updated**: 2026-03-29  
**Status**: ⏳ Awaiting GitHub Actions build result

