package com.cpa.cpasongs
import android.content.Context
import androidx.activity.compose.BackHandler
import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.googlefonts.Font
import androidx.compose.ui.text.googlefonts.GoogleFont
import com.cpa.cpasongs.shared.R
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import java.io.File
private var appContext: Context? = null
actual fun initializePlatform(context: Any) {
    appContext = (context as? Context)?.applicationContext
}
actual suspend fun readAssetFile(path: String): String? = withContext(Dispatchers.IO) {
    try {
        appContext?.assets?.open(path)?.bufferedReader(Charsets.UTF_8)?.use { it.readText() }
    } catch (e: Exception) {
        platformLog("CPA_PLATFORM", "readAssetFile($path) failed: ${'$'}{e.message}")
        null
    }
}
actual suspend fun readCacheFile(fileName: String): String? = withContext(Dispatchers.IO) {
    try {
        val file = File(appContext?.filesDir, fileName)
        if (file.exists()) file.readText(Charsets.UTF_8) else null
    } catch (e: Exception) {
        null
    }
}
actual suspend fun writeCacheFile(fileName: String, content: String): Unit = withContext(Dispatchers.IO) {
    try {
        val dir = appContext?.filesDir ?: return@withContext
        File(dir, fileName).writeText(content, Charsets.UTF_8)
    } catch (e: Exception) { }
}

actual suspend fun readSongVersion(): Long = withContext(Dispatchers.IO) {
    try {
        val prefs = appContext?.getSharedPreferences("cpa_songs_prefs", Context.MODE_PRIVATE)
        prefs?.getLong("songs_version", 0L) ?: 0L
    } catch (e: Exception) {
        0L
    }
}

actual suspend fun writeSongVersion(version: Long): Unit = withContext(Dispatchers.IO) {
    try {
        val prefs = appContext?.getSharedPreferences("cpa_songs_prefs", Context.MODE_PRIVATE)
        prefs?.edit()?.putLong("songs_version", version)?.apply()
    } catch (e: Exception) { }
}

actual fun platformLog(tag: String, message: String) {
    android.util.Log.d(tag, message)
}
actual fun currentTimeMillis(): Long = System.currentTimeMillis()
@Composable
actual fun BackHandlerEffect(enabled: Boolean, onBack: () -> Unit) {
    BackHandler(enabled = enabled, onBack = onBack)
}
@Composable
actual fun urduFontFamily(): FontFamily {
    val provider = remember {
        GoogleFont.Provider(
            providerAuthority = "com.google.android.gms.fonts",
            providerPackage = "com.google.android.gms",
            certificates = R.array.com_google_android_gms_fonts_certs
        )
    }
    return remember {
        FontFamily(Font(GoogleFont("Noto Nastaliq Urdu"), provider))
    }
}
