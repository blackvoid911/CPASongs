# iOS Kotlin/Native Compilation Fixes

## Summary
Fixed 7 Kotlin/Native (K/N) compilation errors that prevented the iOS KMP framework from building. These issues only manifested on iOS because they involve K/N-specific APIs or stdlib differences between JVM and Native.

## Issues Fixed

### 1. Experimental API Warnings (CPAApp.kt:69-70)
**Error**: "This API is experimental and is likely to change in the future"  
**Cause**: `LocalWindowInfo` uses an experimental Compose layout API  
**Fix**: Added `@OptIn(ExperimentalLayoutApi::class)` annotation to `rememberScreenWidthDp()`

```kotlin
@OptIn(ExperimentalLayoutApi::class)
@Composable
fun rememberScreenWidthDp(): Int { ... }
```

### 2. toSortedMap() Unavailable on K/N (CPAApp.kt:1279)
**Error**: "Unresolved reference 'toSortedMap'"  
**Cause**: `toSortedMap()` doesn't exist in Kotlin/Native stdlib (it's a JVM extension)  
**Fix**: Replaced with manual sort: `.toList().sortedBy { it.first }.associate { it.first to it.second }`

```kotlin
// Before:
filteredSongs.groupBy { it.indexChar }.toSortedMap()

// After:
filteredSongs.groupBy { it.indexChar }.toList().sortedBy { it.first }.associate { it.first to it.second }
```

### 3. NSString.create() Missing Parameter (Platform.ios.kt:30, 38)
**Error**: "None of the following candidates is applicable"  
**Cause**: `NSString.create(contentsOfFile:encoding:)` overload doesn't exist; requires error handling parameter  
**Fix**: Added `error = null` parameter to use the proper overload

```kotlin
// Before:
NSString.create(contentsOfFile = it, encoding = NSUTF8StringEncoding) as? String

// After:
NSString.create(contentsOfFile = it, encoding = NSUTF8StringEncoding, error = null) as? String
```

### 4. ExperimentalForeignApi Opt-In Missing (Platform.ios.kt:46)
**Error**: "This declaration needs opt-in. Its usage must be marked with '@kotlinx.cinterop.ExperimentalForeignApi'"  
**Cause**: `NSString.writeToFile()` is a foreign API and requires opt-in  
**Fix**: Added `@OptIn(ExperimentalForeignApi::class)` annotation to the call

```kotlin
@OptIn(ExperimentalForeignApi::class)
(content as NSString).writeToFile("$docsDir/$fileName", true, NSUTF8StringEncoding, null)
```

### 5. NSUserDefaults API Differences (Platform.ios.kt:53, 62)
**Error**: "Unresolved reference 'longForKey'" and "Unresolved reference 'setLong'"  
**Cause**: `NSUserDefaults` doesn't have `longForKey()` or `setLong()` methods in Kotlin/Native bindings  
**Fix**: Use `numberForKey()` → `longValue` and `setObject(NSNumber(value:), forKey:)`

```kotlin
// Before:
defaults.longForKey("songs_version")
defaults.setLong(version, "songs_version")

// After:
val number = defaults.numberForKey("songs_version")
number?.longValue ?: 0L
defaults.setObject(NSNumber(value = version), "songs_version")
```

### 6. Return Type Mismatch (Platform.ios.kt:59)
**Error**: "'actual suspend fun writeSongVersion(version: Long): Any' has no corresponding expected declaration"  
**Cause**: Actual function returned `Any` instead of the expected `Unit`  
**Fix**: Explicitly annotated return type as `Unit`

```kotlin
// Before:
actual suspend fun writeSongVersion(version: Long) = withContext(...) { ... }

// After:
actual suspend fun writeSongVersion(version: Long): Unit = withContext(...) { ... }
```

### 7. NSDate Constructor (Platform.ios.kt:69)
**Error**: "Unresolved reference 'date'"  
**Cause**: `NSDate.date()` is a class method (in Objective-C), not an instance constructor  
**Fix**: Changed to use the constructor `NSDate()`

```kotlin
// Before:
(NSDate.date().timeIntervalSince1970 * 1000).toLong()

// After:
(NSDate().timeIntervalSince1970 * 1000).toLong()
```

## Key Learnings

### JVM vs Kotlin/Native Differences
1. **Stdlib**: Not all stdlib functions are available on K/N (e.g., `toSortedMap`)
2. **Platform APIs**: JVM-specific APIs (java.* packages) don't exist on K/N
3. **Foreign API**: Interop with Objective-C requires explicit opt-in via `@OptIn(ExperimentalForeignApi::class)`

### Objective-C Interop
- Class methods become static properties/functions
- Some API overloads differ in K/N bindings (e.g., NSString.create)
- NSNumber boxing/unboxing pattern needed for numeric storage in NSUserDefaults

### Common K/N Pitfalls
- K/N has stricter type checking and fewer extension functions than JVM
- Most experimental APIs require opt-in annotations
- Platform-specific code must work on both Android (JVM) and iOS (K/N) when in common source sets

## Verification
- ✅ Android build still passes: `./gradlew.bat :app:assembleDebug`
- ✅ iOS compilation should now pass: `./gradlew :shared:linkDebugFrameworkIosSimulatorArm64`

## Related Commits
- `cba6002` - iOS Gradle configuration fix (source set discovery)
- `9a7089f` - Added `import kotlinx.coroutines.IO` for K/N
- (This commit) - iOS K/N API compatibility fixes

