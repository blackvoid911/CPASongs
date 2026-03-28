# Add project specific ProGuard rules here.
# You can control the set of applied configuration files using the
# proguardFiles setting in build.gradle.
#
# For more details, see
#   http://developer.android.com/guide/developing/tools/proguard.html

# If your project uses WebView with JS, uncomment the following
# and specify the fully qualified class name to the JavaScript interface
# class:
#-keepclassmembers class fqcn.of.javascript.interface.for.webview {
#   public *;
#}

# Uncomment this to preserve the line number information for
# debugging stack traces.
-keepattributes SourceFile,LineNumberTable

# If you keep the line number information, uncomment this to
# hide the original source file name.
-renamesourcefileattribute SourceFile

# Keep Gson classes
-keepattributes Signature
-keepattributes *Annotation*
-keepattributes EnclosingMethod
-keepattributes InnerClasses
-keep class com.google.gson.** { *; }
-keep class * implements com.google.gson.TypeAdapterFactory
-keep class * implements com.google.gson.JsonSerializer
-keep class * implements com.google.gson.JsonDeserializer

# Keep Gson TypeToken (needed for generic type parsing - critical for R8 full mode)
-keep class com.google.gson.reflect.TypeToken { *; }
-keep class * extends com.google.gson.reflect.TypeToken
-keep,allowobfuscation,allowshrinking class com.google.gson.reflect.TypeToken

# Keep anonymous TypeToken subclasses used in parseJsonToSongs
-keepclassmembers class com.cpa.cpasongs.MainActivityKt {
    *** parseJsonToSongs(...);
}

# Keep Java collections generic signatures (Gson needs these at runtime)
-keep class java.util.Map { *; }
-keep class java.util.List { *; }
-keep class java.util.HashMap { *; }
-keep class java.util.ArrayList { *; }

# Keep HttpURLConnection (used for GitHub song sync)
-keep class java.net.HttpURLConnection { *; }
-keep class javax.net.ssl.HttpsURLConnection { *; }

# Keep ALL data classes used with Gson for JSON parsing
# Song data classes
-keep class com.cpa.cpasongs.SongItem { *; }
-keepclassmembers class com.cpa.cpasongs.SongItem { *; }

# Bible data classes
-keep class com.cpa.cpasongs.BibleBookData { *; }
-keepclassmembers class com.cpa.cpasongs.BibleBookData { *; }
-keep class com.cpa.cpasongs.BibleChapterData { *; }
-keepclassmembers class com.cpa.cpasongs.BibleChapterData { *; }
-keep class com.cpa.cpasongs.BibleVerse { *; }
-keepclassmembers class com.cpa.cpasongs.BibleVerse { *; }
-keep class com.cpa.cpasongs.BibleChapter { *; }
-keepclassmembers class com.cpa.cpasongs.BibleChapter { *; }
-keep class com.cpa.cpasongs.BibleBook { *; }
-keepclassmembers class com.cpa.cpasongs.BibleBook { *; }
-keep class com.cpa.cpasongs.BibleSearchResult { *; }
-keepclassmembers class com.cpa.cpasongs.BibleSearchResult { *; }

# Keep all data classes in the package (safety net)
-keep class com.cpa.cpasongs.** { *; }
-keepclassmembers class com.cpa.cpasongs.** {
    <fields>;
    <methods>;
}

# Keep Map and List types used in Gson parsing
-keepclassmembers class * {
    @com.google.gson.annotations.SerializedName <fields>;
}

# Retrofit (if used in future)
-dontwarn retrofit2.**
-keep class retrofit2.** { *; }

# OkHttp
-dontwarn okhttp3.**
-dontwarn okio.**

# SLF4J (pulled in by Ktor)
-dontwarn org.slf4j.impl.StaticLoggerBinder

# Ktor
-dontwarn io.ktor.**
-keep class io.ktor.** { *; }

# kotlinx.serialization
-keepattributes RuntimeVisibleAnnotations
-keep class kotlinx.serialization.** { *; }
-keepclassmembers class * {
    @kotlinx.serialization.Serializable *;
}
-keep @kotlinx.serialization.Serializable class * { *; }

