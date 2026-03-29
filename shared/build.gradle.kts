import org.jetbrains.kotlin.gradle.dsl.JvmTarget

plugins {
    alias(libs.plugins.kotlin.multiplatform)
    alias(libs.plugins.android.library)
    alias(libs.plugins.compose.multiplatform)
    alias(libs.plugins.kotlin.compose)
    alias(libs.plugins.kotlin.serialization)
}

// iOS targets only compile on macOS (requires Apple linker tools).
// Modern macOS returns "Mac OS X"; match case-insensitively for safety.
val osName = System.getProperty("os.name") ?: ""
val isRunningOnMac = osName.contains("Mac OS", ignoreCase = true)

kotlin {
    // Global opt-in for experimental APIs used across source sets.
    // This avoids per-call @OptIn annotations that are easy to miss.
    sourceSets.configureEach {
        languageSettings {
            optIn("kotlinx.cinterop.ExperimentalForeignApi")
            optIn("androidx.compose.foundation.layout.ExperimentalLayoutApi")
            optIn("androidx.compose.ui.ExperimentalComposeUiApi")
        }
    }

    androidTarget {
        compilerOptions {
            jvmTarget.set(JvmTarget.JVM_11)
        }
    }

    if (isRunningOnMac) {
        listOf(
            iosX64(),
            iosArm64(),
            iosSimulatorArm64()
        ).forEach { iosTarget ->
            iosTarget.binaries.framework {
                baseName = "shared"
                isStatic = true
            }
        }

        // Explicitly ensure the default hierarchy (iosMain etc.) is created.
        // Kotlin 2.0 applies this by default, but calling it explicitly is a
        // safety-net for Gradle 9.x where lazy source-set creation can race.
        @OptIn(org.jetbrains.kotlin.gradle.ExperimentalKotlinGradlePluginApi::class)
        applyDefaultHierarchyTemplate()
    }

    sourceSets {
        commonMain.dependencies {
            implementation(compose.runtime)
            implementation(compose.foundation)
            implementation(compose.material3)
            implementation(compose.ui)
            implementation(compose.components.resources)
            @OptIn(org.jetbrains.compose.ExperimentalComposeLibrary::class)
            implementation(compose.materialIconsExtended)
            implementation(libs.ktor.client.core)
            implementation(libs.kotlinx.serialization.json)
            implementation(libs.kotlinx.coroutines.core)
        }

        androidMain.dependencies {
            implementation(libs.ktor.client.cio)
            implementation(libs.androidx.compose.ui.text.google.fonts)
            implementation(libs.androidx.activity.compose)
        }
    }
}

// Configure iOS dependencies safely.
// configureEach is lazy — it applies the action whenever a matching source set
// is realised, so it cannot fail if iosMain hasn't been registered yet.
if (isRunningOnMac) {
    kotlin.sourceSets.configureEach {
        if (name == "iosMain") {
            dependencies {
                implementation(libs.ktor.client.darwin)
            }
        }
    }
}

android {
    namespace = "com.cpa.cpasongs.shared"
    compileSdk = 36

    defaultConfig {
        minSdk = 24
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_11
        targetCompatibility = JavaVersion.VERSION_11
    }
}

compose.resources {
    // Fix: project name "CPA Songs" has a space which breaks default package generation
    packageOfResClass = "com.cpa.cpasongs.shared.generated.resources"
    generateResClass = always
}
