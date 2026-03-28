# AGENTS.md
## Project snapshot
- `CPASongs` is a **Kotlin Multiplatform (KMP)** project using **Compose Multiplatform + Material 3**, targeting **Android** and **iOS**.
- Two Gradle modules: `:app` (Android shell) and `:shared` (all UI, state, asset loading, networking, navigation).
- Package name is **`com.cpa.cpasongs`** (previously `com.example`; changed for Google Play).
- The app is a **multi-screen church companion** with Song Book and Bible Reader.
- All composables, data classes, and business logic live in `shared/src/commonMain/kotlin/com/cpa/cpasongs/CPAApp.kt`.
- Platform-specific code (file I/O, fonts, back handler) is split across `expect`/`actual` declarations in `Platform.kt` (common), `Platform.android.kt`, and `Platform.ios.kt`.
- Do **not** assume MVVM/repository usage just because `SongRepository.kt`, `SongApiService.kt`, and `Song.kt` exist in `:app`; they are legacy and unreferenced by the Compose UI.

## Look here first
- `shared/src/commonMain/kotlin/com/cpa/cpasongs/CPAApp.kt` — **all screens** (home, song book, Bible reader), state machine, data models, networking, asset parsing.
- `shared/src/commonMain/kotlin/com/cpa/cpasongs/Platform.kt` — `expect` declarations for platform APIs (file I/O, logging, fonts, back handler, time).
- `shared/src/androidMain/kotlin/com/cpa/cpasongs/Platform.android.kt` — Android `actual` implementations (Context-based file I/O, Google Fonts Noto Nastaliq Urdu, `BackHandler`).
- `shared/src/iosMain/kotlin/com/cpa/cpasongs/Platform.ios.kt` — iOS `actual` implementations (NSBundle asset reading, NSDocumentDirectory caching).
- `shared/src/iosMain/kotlin/com/cpa/cpasongs/MainViewController.kt` — iOS entry point (`ComposeUIViewController`).
- `app/src/main/java/com/cpa/cpasongs/MainActivity.kt` — **thin Android launcher** (~25 lines): calls `initializePlatform(this)` then `setContent { CPAMainApp() }`.
- `shared/src/commonMain/kotlin/com/cpa/cpasongs/ui/theme/` — navy-blue/gradient palette (light + dark), Material 3 theme wiring (Color.kt, Theme.kt, Type.kt).
- `shared/src/commonMain/composeResources/drawable/` — shared image resources (e.g. `ic_launcher_foreground.webp`).
- `app/src/main/assets/urdusongs.json` and `app/src/main/assets/englishsongs.json` — song content.
- `app/src/main/assets/bible/` — offline KJV Bible (66 English JSON files + `urdu/` subdirectory with Urdu translations + `index.json`).
- `shared/build.gradle.kts` — KMP targets (androidTarget + iOS), Compose Multiplatform, Ktor, kotlinx.serialization.
- `app/build.gradle.kts`, `gradle/libs.versions.toml`, `app/src/main/AndroidManifest.xml` — Android app dependencies, versions, permissions, and network security config.
- `app/proguard-rules.pro` — R8/ProGuard rules critical for release builds: Gson TypeToken (legacy), Ktor/SLF4J dontwarn, and kotlinx.serialization keep rules.
- `iosApp/` — Xcode project with SwiftUI shell that hosts the KMP shared framework.

## Actual data flow
- `MainActivity` (Android) or `MainViewController` (iOS) renders `CPAMainApp()`.
- `CPAMainApp()` initializes the Urdu font via `urduFontFamily()` (platform expect/actual), wraps in `CPASongsTheme`, and provides `LocalUrduFont` via `CompositionLocalProvider`.
- `CPAMainAppContent()` owns a `Screen` enum (`HOME`, `SONG_BOOK`, `BIBLE_READER`) and delegates to `HomeMenuScreen`, `SongBookApp`, or `BibleScreen`. Screen transitions use horizontal **slide animations** via `AnimatedContent`.
- **Home** — `HomeMenuScreen` shows the CPA logo (loaded via `painterResource(Res.drawable.ic_launcher_foreground)` from shared compose resources), organization name, a Bible verse, mission statement, and two menu cards (Song Book, Bible).
- **Songs** — `SongBookApp()` loads songs once in `LaunchedEffect(Unit)` via `loadSongsAsync()` (no context param) and keeps navigation in local Compose state: `selectedSong`, `selectedLetter`, `selectedTab`, `searchQuery`, `isSearching`.
- `loadSongsAsync()` uses a **3-tier strategy**: (1) CPA-PK.org API with version check + incremental sync (`SongApi.BASE_URL`) via **Ktor HttpClient**, (2) read local unified cache file (`cached_songs.json`) via `readCacheFile()`, (3) fall back to bundled assets (`urdusongs.json`, `englishsongs.json`) via `readAssetFile()` using legacy parser. The API sync checks version on every app open; if version differs, it calls `?export=1` (first install) or `?since=TIMESTAMP` (incremental). Downloaded JSON updates/inserts/deletes by `id` and respects `is_active` flag. Sync is non-blocking — cached songs display instantly while API updates in background.
- `SongApi` points to `https://cpa-pk.org/pages/api/songs.php` with three endpoints: `?version=1` (version check), `?export=1` (full grouped export), `?since=TIMESTAMP` (incremental changes). To update songs in the live app, modify the server database; changes propagate on next app open via incremental sync. Deletions work via `is_active = 0` in the API response.
- Song JSON from API has `id`, `title`, `author`, `category` (`zaboor`/`geet`/`english`), `song_number`, `sort_order`, `is_active`, `version`, `updated_at`, `lyrics`. The `SongRaw` data class uses **kotlinx.serialization**. Export endpoint returns grouped `{ songs: { zaboor: [...], geet: [...], english: [...] } }`; incremental endpoint returns flat `{ songs: [...] }`.
- Category mapping: API `zaboor` → `"Psalm"` + `"Urdu"`; `geet` → `"Song"` + `"Urdu"`; `english` → `"Song"` + `"English"`. The UI tabs are still `All`, `English`, `Geet`, `Zaboor`.
- IDs are now **stable server-assigned integers** (not synthetic), used for incremental sync upsert/delete by ID. Version tracking uses `readSongVersion()` / `writeSongVersion()` (expect/actual) to store a `Long` timestamp in platform-specific persistent storage (Android SharedPreferences, iOS NSUserDefaults).
- **Bible** — `BibleScreen` loads chapter data on-demand via `BibleStorage.loadBookFromAssets()`, which reads per-book JSON via `readAssetFile("bible/$fileName")` or `readAssetFile("bible/urdu/$fileName")`. Each JSON contains `{ book, chapters: [{ chapter, verses: [{ verse, text }] }] }`. Parsed via **kotlinx.serialization** (`BibleBookData`, `BibleChapterData`, `BibleVerse` — all `@Serializable`).
- `BibleStorage.getBookFileName()` maps book names to file names (spaces removed, lowercase). The hardcoded book lists (`oldTestamentBooks`, `newTestamentBooks`) include English name, Urdu name, testament code, and chapter count.
- Bible search (`searchBibleVerses`) searches **both English and Urdu** testaments simultaneously (ignores `language` param), uses `contains(query, ignoreCase = true)` for proper Urdu Unicode matching, and caps results at 100. Each result stores its actual language for proper RTL rendering in search results.

## Platform expect/actual pattern
The shared module uses Kotlin `expect`/`actual` for platform-specific operations:
| expect function | Android actual | iOS actual |
|---|---|---|
| `initializePlatform(context)` | Stores `Context` | No-op |
| `readAssetFile(path)` | `context.assets.open(path)` | `NSBundle.mainBundle.pathForResource` |
| `readCacheFile(fileName)` | `File(filesDir, name).readText()` | `NSDocumentDirectory` read |
| `writeCacheFile(fileName, content)` | `File(filesDir, name).writeText()` | `NSDocumentDirectory` write |
| `readSongVersion()` | `SharedPreferences.getLong("songs_version")` | `NSUserDefaults.longForKey("songs_version")` |
| `writeSongVersion(version)` | `SharedPreferences.putLong("songs_version")` | `NSUserDefaults.setLong("songs_version")` |
| `platformLog(tag, message)` | `android.util.Log.d()` | `println()` |
| `currentTimeMillis()` | `System.currentTimeMillis()` | `NSDate.date().timeIntervalSince1970 * 1000` |
| `BackHandlerEffect(enabled, onBack)` | `BackHandler` (activity-compose) | No-op (iOS swipe-back) |
| `urduFontFamily()` | Google Fonts `Noto Nastaliq Urdu` | `FontFamily.Default` (see note in file) |

## UI conventions to preserve
- Top-level song tabs are: `All`, `English`, `Geet`, `Zaboor` (default is `Geet`, index 2).
- Urdu detection uses `isUrduText()` (`0x0600..0x06FF`) and affects both font choice and layout direction.
- Urdu text uses `LocalUrduFont.current` throughout composables. On Android this resolves to Google Fonts `Noto Nastaliq Urdu`; on iOS it falls back to system font (until a bundled TTF is added).
- `SongListItem()` preserves original title casing (no uppercasing).
- `SongDetailScreen()` centers lyrics and uses much larger Urdu spacing (`lineHeight = 52.sp`).
- `SongItem.isPunjabi` is computed during import but is currently unused in the UI.
- Bible reader supports an English/Urdu language toggle, adjustable font size (A-/A+), chapter navigation, and full-text verse search.
- Responsive column counts adapt to screen width via `rememberScreenWidthDp()` (uses `LocalWindowInfo.current.containerSize` — multiplatform replacement for `LocalConfiguration.current.screenWidthDp`).

## Legacy code and integration notes
- `SongApiService.kt` still points to `http://10.0.2.2/cpa/pages/songs.php`; `INTERNET` permission exists for song downloads and this legacy path. Cleartext is disabled globally (`usesCleartextTraffic="false"`) but allowed for `10.0.2.2` via `network_security_config.xml`.
- `Song.kt` defines a separate `Song` data class (used by `SongApiService`/`SongRepository`); the active UI uses the `SongItem` data class in `CPAApp.kt`. Do not confuse the two.
- `SongRepository.kt` contains sample hardcoded songs. Neither `SongApiService` nor `SongRepository` is referenced by the current Compose UI.
- Release builds enable R8 minification and resource shrinking (`isMinifyEnabled = true`, `isShrinkResources = true`).
- Boilerplate test files (`ExampleUnitTest.kt`, `ExampleInstrumentedTest.kt`) still use the old `com.example.cpasongs` package; they compile but the instrumented test's package-name assertion would fail against the real app.
- Signing config for release is checked into `app/build.gradle.kts` with keystore `cpasongs-release-key.keystore`.
- Current version: **1.0.4** (versionCode **5**). Bump `versionCode` in `app/build.gradle.kts` before every Play Store upload — Google rejects duplicate codes.
- `shared/src/androidMain/res/values/font_certs.xml` — Google Fonts certificate file (copied from app module, needed by `Platform.android.kt`).

## Build and validation workflow
- **Critical build config**: The `:app` module depends on `project(":shared")`. The `settings.gradle.kts` includes `maven("https://maven.pkg.jetbrains.space/public/p/compose/dev")` in both `pluginManagement` and `dependencyResolutionManagement` repos — required for Compose Multiplatform plugin resolution.
- **Version catalog** (`gradle/libs.versions.toml`): Defines all KMP plugins (`kotlin-multiplatform`, `android-library`, `compose-multiplatform`, `kotlin-serialization`, `kotlin-android`) and libraries (`ktor-client-core`, `ktor-client-cio`, `ktor-client-darwin`, `kotlinx-serialization-json`, `kotlinx-coroutines-core`). All are declared `apply false` in the root `build.gradle.kts`.
- **JVM target alignment**: Both `:app` and `:shared` target JVM 11. The `:app` module sets `kotlinOptions { jvmTarget = "11" }` to match `compileOptions`. The `:shared` module sets it via `compilerOptions { jvmTarget.set(JvmTarget.JVM_11) }`.
- Verified on Windows from repo root; terminal builds needed a JDK explicitly set:
```powershell
$env:JAVA_HOME = 'C:\Program Files\Android\Android Studio\jbr'
$env:Path = "$env:JAVA_HOME\bin;$env:Path"
.\gradlew.bat :shared:compileDebugKotlinAndroid   # shared module only
.\gradlew.bat :app:assembleDebug                   # full Android APK
.\gradlew.bat :app:bundleRelease                    # signed release AAB for Play Store
.\gradlew.bat testDebugUnitTest
.\gradlew.bat lintDebug
```
- **iOS builds require macOS** with Xcode 15+. The `shared/build.gradle.kts` conditionally enables iOS targets only when `os.name` starts with `Mac OS`. On Windows, iOS source sets are skipped — this is intentional.
- To build the iOS app on macOS:
```bash
cd iosApp
xcodebuild -project iosApp.xcodeproj -scheme iosApp -sdk iphonesimulator build
# Or open iosApp.xcodeproj in Xcode and run on simulator/device
```
- The Xcode project includes a "Build KMP Shared Framework" script phase that runs `./gradlew :shared:linkDebugFrameworkIosSimulatorArm64` (debug) or `:shared:linkReleaseFrameworkIosArm64` (release).
- `connectedDebugAndroidTest` is only useful when a device/emulator is available.
- Current tests are still boilerplate (`ExampleUnitTest`, `ExampleInstrumentedTest`), so behavior changes should be checked mainly through builds and manual UI verification.

## iOS-specific notes
- **Bible & song asset files** must be added to the iOS app bundle. Copy the `app/src/main/assets/` contents (`urdusongs.json`, `englishsongs.json`, `bible/` folder) into `iosApp/iosApp/` and add them to the Xcode target's "Copy Bundle Resources" build phase.
- **Urdu font**: To get proper Nastaliq rendering on iOS, download `NotoNastaliqUrdu-Regular.ttf` from Google Fonts, add it to `iosApp/iosApp/`, register in `Info.plist` under `UIAppFonts`, then update `Platform.ios.kt` to use `FontFamily(Font("NotoNastaliqUrdu-Regular"))`.
- **App icon**: Replace placeholder in `iosApp/iosApp/Assets.xcassets/AppIcon.appiconset/` with a 1024×1024 PNG.
- iOS bundle identifier: `com.cpa.cpasongs.ios` (set in Xcode project).
- **iOS builds on Windows**: GitHub Actions workflows (`.github/workflows/build-multiplatform.yml`, `build-ios.yml`) automatically build iOS on macOS-14 runners with Xcode 15. Push to main/develop triggers builds; download artifacts (iOS .app, unsigned IPA) from Actions tab. Local macOS builds use `./build-ios.sh simulator` or open `iosApp.xcodeproj` in Xcode.

## Change guidance
- All UI changes go in `shared/src/commonMain/kotlin/com/cpa/cpasongs/CPAApp.kt` — both Android and iOS share this file.
- Platform-specific changes (file I/O, fonts, native APIs) go in the corresponding `Platform.android.kt` or `Platform.ios.kt`.
- `app/src/main/java/com/cpa/cpasongs/MainActivity.kt` is a thin launcher (~25 lines) — avoid adding logic here.
- If you change the song schema, update the `SongRaw` data class and corresponding parsing logic in `CPAApp.kt`.
- Preserve Urdu/RTL behavior when touching title rendering, grouping, ordering, or list/detail layout.
- **API song updates**: Songs sync from `https://cpa-pk.org/pages/api/songs.php`. To update songs, modify the server database; changes propagate on next app open via incremental sync (`?since=TIMESTAMP`). No app rebuild needed.
- **Serialization**: Song and Bible JSON parsing uses `kotlinx.serialization`. All data classes (`SongRaw`, `BibleBookData`, `BibleChapterData`, `BibleVerse`) must have `@Serializable` annotation and default values for all fields.
- **Networking**: HTTP calls use **Ktor** `HttpClient` (CIO engine on Android, Darwin engine on iOS). The engine is selected via `androidMain`/`iosMain` dependencies in `shared/build.gradle.kts`.
- **ProGuard / R8**: `proguard-rules.pro` keeps Gson `TypeToken` generic signatures (legacy), Ktor/SLF4J dontwarn rules, and kotlinx.serialization keep rules. All are needed for R8 release builds. If you add new serialized types, add corresponding `-keep` rules.
- **AGP 9.0 compatibility**: `gradle.properties` sets `android.builtInKotlin=false` and `android.newDsl=false` to allow `com.android.library` + `kotlin.multiplatform` together in the `:shared` module. This is a temporary workaround; future AGP versions may require `com.android.kotlin.multiplatform.library`.
- **Compose Resources**: The project name "CPA Songs" contains a space, so `compose.resources.packageOfResClass` is explicitly set to `com.cpa.cpasongs.shared.generated.resources` in `shared/build.gradle.kts`. Shared drawables go in `shared/src/commonMain/composeResources/drawable/` and are accessed via `Res.drawable.*`.
