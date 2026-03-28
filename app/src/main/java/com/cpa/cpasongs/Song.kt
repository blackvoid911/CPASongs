package com.cpa.cpasongs

data class Song(
    val id: Int,
    val title: String,
    val lyrics: String,
    val language: String,
    val category: String = "Song",
    val indexChar: String = "#",
    val heading: String? = null
)
