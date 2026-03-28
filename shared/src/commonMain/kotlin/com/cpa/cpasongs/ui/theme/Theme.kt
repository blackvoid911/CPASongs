package com.cpa.cpasongs.ui.theme

import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable

private val LightColorScheme = lightColorScheme(
    primary = GradientEnd,
    onPrimary = LightSurface,
    primaryContainer = GradientStart,
    onPrimaryContainer = LightSurface,
    secondary = GradientMid,
    onSecondary = LightSurface,
    secondaryContainer = LightSurfaceVariant,
    onSecondaryContainer = LightOnSurface,
    tertiary = GradientStart,
    onTertiary = LightSurface,
    tertiaryContainer = GradientMid,
    onTertiaryContainer = LightSurface,
    background = LightBackground,
    onBackground = LightOnBackground,
    surface = LightSurface,
    onSurface = LightOnSurface,
    surfaceVariant = LightSurfaceVariant,
    onSurfaceVariant = LightOnSurfaceVariant,
    outline = LightOutline,
    outlineVariant = LightDivider
)

private val DarkColorScheme = darkColorScheme(
    primary = GradientStart,
    onPrimary = DarkBackground,
    primaryContainer = GradientEnd,
    onPrimaryContainer = DarkOnSurface,
    secondary = GradientMid,
    onSecondary = DarkBackground,
    secondaryContainer = DarkSurfaceVariant,
    onSecondaryContainer = DarkOnSurface,
    tertiary = GradientStart,
    onTertiary = DarkBackground,
    tertiaryContainer = GradientMid,
    onTertiaryContainer = DarkOnSurface,
    background = DarkBackground,
    onBackground = DarkOnBackground,
    surface = DarkSurface,
    onSurface = DarkOnSurface,
    surfaceVariant = DarkSurfaceVariant,
    onSurfaceVariant = DarkOnSurfaceVariant,
    outline = DarkOutline,
    outlineVariant = DarkDivider
)

@Composable
fun CPASongsTheme(
    darkTheme: Boolean = isSystemInDarkTheme(),
    content: @Composable () -> Unit
) {
    val colorScheme = if (darkTheme) DarkColorScheme else LightColorScheme

    MaterialTheme(
        colorScheme = colorScheme,
        typography = Typography,
        content = content
    )
}

