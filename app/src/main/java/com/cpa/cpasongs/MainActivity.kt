package com.cpa.cpasongs

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge

/**
 * Android entry point.
 * All UI + logic lives in :shared (CPAApp.kt / commonMain).
 * This file is intentionally minimal.
 */
class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        // Initialize platform services (Android Context) before any coroutine runs
        initializePlatform(this)
        enableEdgeToEdge()
        setContent {
            // CPAMainApp is in shared/commonMain and includes CPASongsTheme internally
            CPAMainApp()
        }
    }
}
