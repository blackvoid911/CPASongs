package com.cpa.cpasongs
import androidx.compose.ui.window.ComposeUIViewController
/**
 * Entry point called by Swift/SwiftUI in iosApp/ContentView.swift.
 * Returns a UIViewController hosting CPAMainApp() via Compose Multiplatform.
 */
fun MainViewController() = ComposeUIViewController {
    CPAMainApp()
}
