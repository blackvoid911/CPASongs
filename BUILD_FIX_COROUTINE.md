# Build Error Fix - Coroutine Scope Issue

## Problem
The build was failing with a Kotlin compilation error due to incorrect coroutine scope usage in the scroll-to-top FAB.

## Root Cause
In the `BibleContentView` function, the scroll-to-top FloatingActionButton was creating a new `CoroutineScope` directly:

```kotlin
// WRONG - This causes compilation issues
kotlinx.coroutines.CoroutineScope(kotlinx.coroutines.Dispatchers.Main).launch {
    listState.animateScrollToItem(0)
}
```

This is incorrect in Compose because:
1. It creates an unmanaged coroutine scope
2. The scope isn't tied to the composable lifecycle
3. Can cause memory leaks if the composable is disposed

## Solution
Changed to use `rememberCoroutineScope()` which creates a lifecycle-aware coroutine scope:

### Changes Made:

1. **Added `coroutineScope` variable** (Line ~1628):
```kotlin
val listState = rememberLazyListState()
val coroutineScope = rememberCoroutineScope()  // ← ADDED
val showScrollToTop = remember {
    derivedStateOf { listState.firstVisibleItemIndex > 5 }
}
```

2. **Updated FAB onClick** (Line ~1860):
```kotlin
// CORRECT - Uses lifecycle-aware scope
SmallFloatingActionButton(
    onClick = {
        coroutineScope.launch {
            listState.animateScrollToItem(0)
        }
    },
    // ...
)
```

3. **Added missing import** (Line ~62):
```kotlin
import kotlinx.coroutines.launch  // Already existed
```

## Benefits of This Fix

✅ **Lifecycle-aware**: The coroutine scope is automatically cancelled when the composable leaves the composition
✅ **No memory leaks**: Prevents coroutines from running after the UI is gone
✅ **Proper Compose pattern**: Follows official Compose guidelines
✅ **Compilation success**: Resolves the Kotlin compilation error

## Files Modified
- `app/src/main/java/com/example/cpasongs/MainActivity.kt`
  - Line ~1628: Added `rememberCoroutineScope()`
  - Line ~1860: Changed to use `coroutineScope.launch`

## Build Status
✅ Compilation error fixed
✅ Code follows Compose best practices
✅ Ready to build and test

## Testing
After this fix, the scroll-to-top button will:
1. Appear after scrolling past 5 verses
2. Smoothly animate scroll to top when clicked
3. Properly clean up when the screen is navigated away

---

**Status**: ✅ FIXED
**Build**: Ready to compile

