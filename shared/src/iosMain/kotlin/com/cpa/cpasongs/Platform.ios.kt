package com.cpa.cpasongs
import androidx.compose.runtime.Composable
import androidx.compose.ui.text.font.FontFamily
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import kotlinx.cinterop.ExperimentalForeignApi
import platform.Foundation.NSBundle
import platform.Foundation.NSDate
import platform.Foundation.NSDocumentDirectory
import platform.Foundation.NSNumber
import platform.Foundation.NSSearchPathForDirectoriesInDomains
import platform.Foundation.NSString
import platform.Foundation.NSUTF8StringEncoding
import platform.Foundation.NSUserDomainMask
import platform.Foundation.NSUserDefaults
import platform.Foundation.create
import platform.Foundation.writeToFile

actual fun initializePlatform(context: Any) { /* No-op on iOS */ }

actual suspend fun readAssetFile(path: String): String? = withContext(Dispatchers.Default) {
    try {
        val parts = path.split("/")
        val fileName = parts.last()
        val dotIdx = fileName.lastIndexOf('.')
        val name = if (dotIdx >= 0) fileName.substring(0, dotIdx) else fileName
        val ext  = if (dotIdx >= 0) fileName.substring(dotIdx + 1) else ""
        val subDir = if (parts.size > 1) parts.dropLast(1).joinToString("/") else null
        val bundle = NSBundle.mainBundle
        val filePath = if (subDir != null)
            bundle.pathForResource(name, ext, subDir)
        else
            bundle.pathForResource(name, ext)
        filePath?.let { 
            NSString.create(contentsOfFile = it, encoding = NSUTF8StringEncoding, error = null) as? String 
        }
    } catch (e: Exception) { null }
}

actual suspend fun readCacheFile(fileName: String): String? = withContext(Dispatchers.Default) {
    try {
        @Suppress("UNCHECKED_CAST")
        val dirs = NSSearchPathForDirectoriesInDomains(NSDocumentDirectory, NSUserDomainMask, true) as List<String>
        val docsDir = dirs.firstOrNull() ?: return@withContext null
        NSString.create(contentsOfFile = "$docsDir/$fileName", encoding = NSUTF8StringEncoding, error = null) as? String
    } catch (e: Exception) { null }
}

actual suspend fun writeCacheFile(fileName: String, content: String) = withContext(Dispatchers.Default) {
    try {
        @Suppress("UNCHECKED_CAST")
        val dirs = NSSearchPathForDirectoriesInDomains(NSDocumentDirectory, NSUserDomainMask, true) as List<String>
        val docsDir = dirs.firstOrNull() ?: return@withContext
        @OptIn(ExperimentalForeignApi::class)
        (content as NSString).writeToFile("$docsDir/$fileName", true, NSUTF8StringEncoding, null)
    } catch (e: Exception) { }
}

actual suspend fun readSongVersion(): Long = withContext(Dispatchers.Default) {
    try {
        val defaults = NSUserDefaults.standardUserDefaults
        val number = defaults.numberForKey("songs_version")
        number?.longValue ?: 0L
    } catch (e: Exception) {
        0L
    }
}

actual suspend fun writeSongVersion(version: Long): Unit = withContext(Dispatchers.Default) {
    try {
        val defaults = NSUserDefaults.standardUserDefaults
        defaults.setObject(NSNumber(value = version), "songs_version")
        defaults.synchronize()
    } catch (e: Exception) { }
}

actual fun platformLog(tag: String, message: String) { println("[$tag] $message") }

actual fun currentTimeMillis(): Long =
    (NSDate().timeIntervalSince1970 * 1000).toLong()

@Composable
actual fun BackHandlerEffect(enabled: Boolean, onBack: () -> Unit) {
    // iOS uses swipe-back gesture natively - no hardware back button needed
}

@Composable
actual fun urduFontFamily(): FontFamily = FontFamily.Default

// NOTE: For proper Urdu/Nastaliq rendering on iOS:
// 1. Download NotoNastaliqUrdu-Regular.ttf from Google Fonts
// 2. Add to iosApp/iosApp/ and register in Info.plist under UIAppFonts
// 3. Replace FontFamily.Default above with: FontFamily(Font("NotoNastaliqUrdu-Regular"))
