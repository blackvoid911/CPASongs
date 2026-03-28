import org.jetbrains.kotlin.gradle.dsl.JvmTarget

plugins {
    alias(libs.plugins.kotlin.multiplatform)
    alias(libs.plugins.android.library)
    alias(libs.plugins.compose.multiplatform)
    alias(libs.plugins.kotlin.compose)
    alias(libs.plugins.kotlin.serialization)
}

// iOS targets only compile on macOS (requires Apple linker tools)
val isRunningOnMac = System.getProperty("os.name")?.startsWith("Mac OS") ?: false

kotlin {
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

        if (isRunningOnMac) {
            val iosMain by getting {
                dependencies {
                    implementation(libs.ktor.client.darwin)
                }
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


