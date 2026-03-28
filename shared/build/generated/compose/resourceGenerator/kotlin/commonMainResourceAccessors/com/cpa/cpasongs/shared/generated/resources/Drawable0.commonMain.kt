@file:OptIn(org.jetbrains.compose.resources.InternalResourceApi::class)

package com.cpa.cpasongs.shared.generated.resources

import kotlin.OptIn
import kotlin.String
import kotlin.collections.MutableMap
import org.jetbrains.compose.resources.DrawableResource
import org.jetbrains.compose.resources.InternalResourceApi

private object CommonMainDrawable0 {
  public val ic_launcher_foreground: DrawableResource by 
      lazy { init_ic_launcher_foreground() }
}

@InternalResourceApi
internal fun _collectCommonMainDrawable0Resources(map: MutableMap<String, DrawableResource>) {
  map.put("ic_launcher_foreground", CommonMainDrawable0.ic_launcher_foreground)
}

internal val Res.drawable.ic_launcher_foreground: DrawableResource
  get() = CommonMainDrawable0.ic_launcher_foreground

private fun init_ic_launcher_foreground(): DrawableResource =
    org.jetbrains.compose.resources.DrawableResource(
  "drawable:ic_launcher_foreground",
    setOf(
      org.jetbrains.compose.resources.ResourceItem(setOf(),
    "composeResources/com.cpa.cpasongs.shared.generated.resources/drawable/ic_launcher_foreground.webp", -1, -1),
    )
)
