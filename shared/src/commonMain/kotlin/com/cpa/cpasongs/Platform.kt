package com.cpa.cpasongs

import androidx.compose.runtime.Composable
import androidx.compose.ui.text.font.FontFamily

/**
 * Called once on app start to initialize platform-specific resources.
 * On Android: pass the Application/Activity Context.
 * On iOS: pass Unit (no-op).
 */
expect fun initializePlatform(context: Any = Unit)

/** Reads a file from bundled assets (Android: assets/, iOS: app bundle). */
expect suspend fun readAssetFile(path: String): String?

/** Reads a file from the persistent local cache directory. */
expect suspend fun readCacheFile(fileName: String): String?

/** Writes a file to the persistent local cache directory. */
expect suspend fun writeCacheFile(fileName: String, content: String)

/** Reads the stored song database version (0L if not set). */
expect suspend fun readSongVersion(): Long

/** Saves the song database version. */
expect suspend fun writeSongVersion(version: Long)

/** Platform logging. */
expect fun platformLog(tag: String, message: String)

/** Current time in milliseconds (used as a cache-buster in HTTP requests). */
expect fun currentTimeMillis(): Long

/**
 * Hardware/software back navigation handler.
 * Android: intercepts the system back button.
 * iOS: no-op (iOS uses swipe-back gesture natively).
 */
@Composable
expect fun BackHandlerEffect(enabled: Boolean, onBack: () -> Unit)

/**
 * Returns the Urdu/Nastaliq font family.
 * Android: downloaded via Google Fonts API.
 * iOS: bundled TTF (falls back to system font until you add the file).
 */
@Composable
expect fun urduFontFamily(): FontFamily


