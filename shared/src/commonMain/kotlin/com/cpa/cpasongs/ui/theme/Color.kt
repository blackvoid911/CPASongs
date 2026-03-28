package com.cpa.cpasongs.ui.theme

import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color

// Primary Brand Colors - Navy Blue
val NavyPrimary = Color(0xFF1B2E4A)         // Main brand color
val NavyLight = Color(0xFF2D4A6E)           // Lighter navy
val NavyDark = Color(0xFF0F1C2E)            // Darker navy
val AccentRed = Color(0xFFDC3545)           // Accent red from logo

// Gradient Colors - Blue gradient like the icon
val GradientStart = Color(0xFF4A90D9)       // Light blue
val GradientEnd = Color(0xFF1E3A5F)         // Dark blue
val GradientMid = Color(0xFF2E5B8A)         // Mid blue

// App Gradient Brush
val AppGradient = Brush.linearGradient(
    colors = listOf(GradientStart, GradientEnd)
)

val AppGradientVertical = Brush.verticalGradient(
    colors = listOf(GradientStart, GradientEnd)
)

// Light Mode Colors
val LightBackground = Color(0xFFF8FAFC)     // Clean off-white with slight blue tint
val LightSurface = Color(0xFFFFFFFF)        // Pure white
val LightSurfaceVariant = Color(0xFFF1F5F9) // Slight blue-gray
val LightOnBackground = Color(0xFF1C1B1F)   // Near black
val LightOnSurface = Color(0xFF1C1B1F)
val LightOnSurfaceVariant = Color(0xFF49454F)
val LightOutline = Color(0xFFE2E8F0)        // Light blue-gray
val LightDivider = Color(0xFFF0F4F8)

// Dark Mode Colors  
val DarkBackground = Color(0xFF0F172A)      // Dark blue-black
val DarkSurface = Color(0xFF1E293B)         // Elevated dark blue surface
val DarkSurfaceVariant = Color(0xFF334155)  // Card surface
val DarkOnBackground = Color(0xFFF1F5F9)    // Off-white text
val DarkOnSurface = Color(0xFFF1F5F9)
val DarkOnSurfaceVariant = Color(0xFF94A3B8)
val DarkOutline = Color(0xFF475569)         // Subtle borders
val DarkDivider = Color(0xFF1E293B)

// Semantic Colors
val ErrorRed = Color(0xFFDC3545)
val SuccessGreen = Color(0xFF28A745)

