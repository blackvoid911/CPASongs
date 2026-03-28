package com.cpa.cpasongs
import androidx.compose.animation.*
import androidx.compose.animation.core.*
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.layout.ExperimentalLayoutApi
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.rememberLazyListState
import androidx.compose.foundation.lazy.grid.GridCells
import androidx.compose.foundation.lazy.grid.LazyVerticalGrid
import androidx.compose.foundation.lazy.itemsIndexed
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.rounded.ArrowBack
import androidx.compose.material.icons.automirrored.rounded.ArrowForward
import androidx.compose.material.icons.automirrored.rounded.KeyboardArrowRight
import androidx.compose.material.icons.rounded.Close
import androidx.compose.material.icons.rounded.Search
import androidx.compose.material.icons.rounded.MusicNote
import androidx.compose.material.icons.rounded.Book
import androidx.compose.material.icons.rounded.KeyboardArrowUp
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.platform.LocalDensity
import androidx.compose.ui.platform.LocalLayoutDirection
import androidx.compose.ui.platform.LocalWindowInfo
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.LayoutDirection
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.cpa.cpasongs.ui.theme.CPASongsTheme
import io.ktor.client.HttpClient
import io.ktor.client.request.get
import io.ktor.client.request.headers
import io.ktor.client.statement.bodyAsText
import io.ktor.http.isSuccess
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.IO
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable
import kotlinx.serialization.builtins.ListSerializer
import kotlinx.serialization.json.Json
import org.jetbrains.compose.resources.painterResource
import com.cpa.cpasongs.shared.generated.resources.Res
import com.cpa.cpasongs.shared.generated.resources.ic_launcher_foreground
// CompositionLocal for Urdu font - initialized inside CPAMainApp
val LocalUrduFont = compositionLocalOf<FontFamily> { FontFamily.Default }
// Helper: multiplatform screen width in dp
@OptIn(ExperimentalLayoutApi::class)
@Composable
fun rememberScreenWidthDp(): Int {
    val density = LocalDensity.current
    val windowInfo = LocalWindowInfo.current
    return remember(windowInfo.containerSize, density) {
        with(density) { windowInfo.containerSize.width.toDp() }.value.toInt()
    }
}
// App Navigation
enum class Screen {
    HOME, SONG_BOOK, BIBLE_READER
}
@OptIn(ExperimentalLayoutApi::class)
@Composable
fun CPAMainApp() {
    val urduFont = urduFontFamily()
    CPASongsTheme {
        CompositionLocalProvider(LocalUrduFont provides urduFont) {
            CPAMainAppContent()
        }
    }
}
@Composable
private fun CPAMainAppContent() {
    var currentScreen by remember { mutableStateOf(Screen.HOME) }
    BackHandlerEffect(enabled = currentScreen != Screen.HOME) {
        currentScreen = Screen.HOME
    }
    AnimatedContent(
        targetState = currentScreen,
        transitionSpec = {
            val goingForward = targetState != Screen.HOME
            if (goingForward) {
                slideInHorizontally { it } togetherWith slideOutHorizontally { -it }
            } else {
                slideInHorizontally { -it } togetherWith slideOutHorizontally { it }
            }
        },
        label = "screenTransition"
    ) { screen ->
        when (screen) {
            Screen.HOME -> HomeMenuScreen(onNavigate = { currentScreen = it })
            Screen.SONG_BOOK -> SongBookApp(onBack = { currentScreen = Screen.HOME })
            Screen.BIBLE_READER -> BibleScreen(onBack = { currentScreen = Screen.HOME })
        }
    }
}

// ============ HOME SCREEN ============

@Composable
fun HomeMenuScreen(onNavigate: (Screen) -> Unit) {
    val screenWidth = rememberScreenWidthDp()
    val isTablet = screenWidth >= 600
    val scrollState = rememberScrollState()

    Scaffold(containerColor = MaterialTheme.colorScheme.background) { padding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .verticalScroll(scrollState),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Spacer(modifier = Modifier.height(if (isTablet) 64.dp else 36.dp))

            // Logo
            Image(
                painter = painterResource(Res.drawable.ic_launcher_foreground),
                contentDescription = "CPA Logo",
                modifier = Modifier.size(if (isTablet) 200.dp else 160.dp)
            )

            Spacer(modifier = Modifier.height(16.dp))

            // Organization name
            Text(
                "Calvary Pentecostal Assemblies",
                style = MaterialTheme.typography.titleLarge.copy(
                    lineHeight = 28.sp,
                    letterSpacing = 0.5.sp
                ),
                fontWeight = FontWeight.Bold,
                color = MaterialTheme.colorScheme.onBackground,
                textAlign = TextAlign.Center,
                modifier = Modifier.padding(horizontal = 24.dp)
            )
            Text(
                "of Pakistan",
                style = MaterialTheme.typography.titleMedium.copy(
                    lineHeight = 24.sp,
                    letterSpacing = 0.5.sp
                ),
                fontWeight = FontWeight.Medium,
                color = MaterialTheme.colorScheme.onBackground.copy(alpha = 0.8f),
                textAlign = TextAlign.Center
            )

            Spacer(modifier = Modifier.height(16.dp))

            // Decorative divider
            Row(
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.Center,
                modifier = Modifier.fillMaxWidth()
            ) {
                Box(Modifier.width(32.dp).height(1.dp).background(
                    brush = Brush.horizontalGradient(listOf(Color.Transparent, MaterialTheme.colorScheme.primary.copy(alpha = 0.4f)))
                ))
                Spacer(Modifier.width(8.dp))
                Box(Modifier.size(6.dp).clip(CircleShape).background(MaterialTheme.colorScheme.primary.copy(alpha = 0.5f)))
                Spacer(Modifier.width(8.dp))
                Box(Modifier.width(32.dp).height(1.dp).background(
                    brush = Brush.horizontalGradient(listOf(MaterialTheme.colorScheme.primary.copy(alpha = 0.4f), Color.Transparent))
                ))
            }

            Spacer(modifier = Modifier.height(16.dp))

            // Bible verse
            Text(
                "\u201CGo ye into all the world, and preach the gospel.\u201D",
                style = MaterialTheme.typography.bodyLarge.copy(
                    lineHeight = 24.sp,
                    fontStyle = FontStyle.Italic
                ),
                fontWeight = FontWeight.Medium,
                color = MaterialTheme.colorScheme.primary,
                textAlign = TextAlign.Center,
                modifier = Modifier.padding(horizontal = 40.dp)
            )
            Spacer(modifier = Modifier.height(4.dp))
            Text(
                "— Mark 16:15",
                style = MaterialTheme.typography.labelMedium,
                color = MaterialTheme.colorScheme.primary.copy(alpha = 0.7f),
                textAlign = TextAlign.Center
            )

            Spacer(modifier = Modifier.height(12.dp))

            // Mission statement
            Text(
                "Spreading faith, hope, and love through worship,\nministry, and community service across Pakistan.",
                style = MaterialTheme.typography.bodySmall.copy(lineHeight = 20.sp),
                color = MaterialTheme.colorScheme.onSurfaceVariant,
                textAlign = TextAlign.Center,
                modifier = Modifier.padding(horizontal = 36.dp)
            )

            Spacer(modifier = Modifier.height(32.dp))

            // Menu cards
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = if (isTablet) 100.dp else 24.dp),
                verticalArrangement = Arrangement.spacedBy(14.dp)
            ) {
                MenuItemCard(
                    icon = Icons.Rounded.MusicNote,
                    title = "Song Book",
                    subtitle = "Geet & Zaboor collection",
                    onClick = { onNavigate(Screen.SONG_BOOK) }
                )
                MenuItemCard(
                    icon = Icons.Rounded.Book,
                    title = "Bible",
                    subtitle = "English & Urdu translations",
                    onClick = { onNavigate(Screen.BIBLE_READER) }
                )
            }

            Spacer(modifier = Modifier.height(32.dp))

            // Footer
            Text(
                "CPA Pakistan",
                style = MaterialTheme.typography.labelSmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.5f),
                textAlign = TextAlign.Center
            )

            Spacer(modifier = Modifier.height(24.dp))
        }
    }
}

@Composable
fun MenuItemCard(icon: ImageVector, title: String, subtitle: String = "", onClick: () -> Unit) {
    Card(
        onClick = onClick,
        modifier = Modifier.fillMaxWidth(),
        shape = RoundedCornerShape(18.dp),
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface),
        elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
    ) {
        Row(
            modifier = Modifier.fillMaxWidth().padding(horizontal = 18.dp, vertical = 18.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Box(
                modifier = Modifier.size(52.dp).clip(RoundedCornerShape(14.dp))
                    .background(brush = Brush.linearGradient(
                        colors = listOf(Color(0xFF4A90D9), Color(0xFF1E3A5F))
                    )),
                contentAlignment = Alignment.Center
            ) {
                Icon(imageVector = icon, contentDescription = title,
                    tint = Color.White, modifier = Modifier.size(26.dp))
            }
            Spacer(modifier = Modifier.width(16.dp))
            Column(modifier = Modifier.weight(1f)) {
                Text(
                    text = title,
                    style = MaterialTheme.typography.titleMedium,
                    fontWeight = FontWeight.SemiBold,
                    color = MaterialTheme.colorScheme.onSurface
                )
                if (subtitle.isNotEmpty()) {
                    Spacer(modifier = Modifier.height(2.dp))
                    Text(
                        text = subtitle,
                        style = MaterialTheme.typography.bodySmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                }
            }
            Icon(
                imageVector = Icons.AutoMirrored.Rounded.KeyboardArrowRight,
                contentDescription = null,
                tint = MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.5f),
                modifier = Modifier.size(22.dp)
            )
        }
    }
}


// ============ BIBLE READER IMPLEMENTATION ============

enum class BibleLanguage(val code: String, val displayName: String) {
    ENGLISH("en", "English"),
    URDU("ur", "\u0627\u064F\u0631\u062F\u064F\u0648")
}

data class BibleBook(
    val id: Int, val name: String, val nameUrdu: String,
    val testament: String, val chapters: Int
) {
    fun getDisplayName(language: BibleLanguage): String =
        if (language == BibleLanguage.URDU) nameUrdu else name
}

@Serializable
data class BibleVerse(val verse: Int = 0, val text: String = "")

data class BibleChapter(val book: String, val chapter: Int, val verses: List<BibleVerse>)

@Serializable
data class BibleBookData(val book: String = "", val chapters: List<BibleChapterData> = emptyList())

@Serializable
data class BibleChapterData(val chapter: Int = 0, val verses: List<BibleVerse> = emptyList())

private val bibleJson = Json { ignoreUnknownKeys = true; isLenient = true }

object BibleStorage {
    suspend fun loadBookFromAssets(
        bookName: String, language: BibleLanguage = BibleLanguage.ENGLISH
    ): BibleBookData? = withContext(Dispatchers.IO) {
        try {
            val fileName = getBookFileName(bookName)
            val folder = if (language == BibleLanguage.URDU) "bible/urdu" else "bible"
            val jsonText = readAssetFile("$folder/$fileName")
            jsonText?.let { bibleJson.decodeFromString<BibleBookData>(it) }
        } catch (e: Exception) {
            platformLog("BIBLE", "Error loading $bookName: ${e.message}")
            null
        }
    }

    suspend fun getChapter(
        bookName: String, chapter: Int, language: BibleLanguage = BibleLanguage.ENGLISH
    ): List<BibleVerse> {
        val bookData = loadBookFromAssets(bookName, language)
        return bookData?.chapters?.find { it.chapter == chapter }?.verses ?: emptyList()
    }

    private fun getBookFileName(bookName: String): String =
        "${bookName.lowercase().replace(" ", "")}.json"
}

val oldTestamentBooks = listOf(
    BibleBook(1, "Genesis", "\u067E\u06CC\u062F\u0627\u0626\u0634", "OT", 50),
    BibleBook(2, "Exodus", "\u062E\u064F\u0631\u0648\u062C", "OT", 40),
    BibleBook(3, "Leviticus", "\u0627\u062D\u0628\u0627\u0631", "OT", 27),
    BibleBook(4, "Numbers", "\u06AF\u0646\u062A\u06CC", "OT", 36),
    BibleBook(5, "Deuteronomy", "\u0627\u0650\u0633\u062A\u0650\u062B\u0646\u0627", "OT", 34),
    BibleBook(6, "Joshua", "\u06CC\u0634\u064F\u0648\u0639", "OT", 24),
    BibleBook(7, "Judges", "\u0642\u064F\u0636\u0627\u06C3", "OT", 21),
    BibleBook(8, "Ruth", "\u0631\u064F\u0648\u062A", "OT", 4),
    BibleBook(9, "1 Samuel", "\u06F1-\u0633\u0645\u0648\u0626\u06CC\u0644", "OT", 31),
    BibleBook(10, "2 Samuel", "\u06F2-\u0633\u0645\u0648\u0626\u06CC\u0644", "OT", 24),
    BibleBook(11, "1 Kings", "\u06F1-\u0633\u0644\u0627\u0637\u06CC\u0646", "OT", 22),
    BibleBook(12, "2 Kings", "\u06F2-\u0633\u0644\u0627\u0637\u06CC\u0646", "OT", 25),
    BibleBook(13, "1 Chronicles", "\u06F1-\u062A\u0648\u0627\u0631\u06CC\u062E", "OT", 29),
    BibleBook(14, "2 Chronicles", "\u06F2-\u062A\u0648\u0627\u0631\u06CC\u062E", "OT", 36),
    BibleBook(15, "Ezra", "\u0639\u0632\u0631\u0627", "OT", 10),
    BibleBook(16, "Nehemiah", "\u0646\u062D\u0645\u06CC\u0627\u06C1", "OT", 13),
    BibleBook(17, "Esther", "\u0622\u0633\u062A\u0631", "OT", 10),
    BibleBook(18, "Job", "\u0627\u06CC\u0651\u0648\u0628", "OT", 42),
    BibleBook(19, "Psalms", "\u0632\u0628\u064F\u0648\u0631", "OT", 150),
    BibleBook(20, "Proverbs", "\u0627\u0645\u062B\u0627\u0644", "OT", 31),
    BibleBook(21, "Ecclesiastes", "\u0648\u0627\u0639\u0638", "OT", 12),
    BibleBook(22, "Song of Solomon", "\u063A\u0632\u0644 \u0627\u0644\u063A\u0632\u0644\u0627\u062A", "OT", 8),
    BibleBook(23, "Isaiah", "\u06CC\u0633\u0639\u06CC\u0627\u06C1", "OT", 66),
    BibleBook(24, "Jeremiah", "\u06CC\u0631\u0645\u06CC\u0627\u06C1", "OT", 52),
    BibleBook(25, "Lamentations", "\u0646\u0648\u062D\u06C1", "OT", 5),
    BibleBook(26, "Ezekiel", "\u062D\u0632\u0642\u06CC \u0627\u06CC\u0644", "OT", 48),
    BibleBook(27, "Daniel", "\u062F\u0627\u0646\u06CC \u0627\u06CC\u0644", "OT", 12),
    BibleBook(28, "Hosea", "\u06C1\u0648\u0633\u06CC\u0639", "OT", 14),
    BibleBook(29, "Joel", "\u06CC\u0648\u0627\u06CC\u0644", "OT", 3),
    BibleBook(30, "Amos", "\u0639\u0627\u0645\u0648\u0633", "OT", 9),
    BibleBook(31, "Obadiah", "\u0639\u0628\u062F\u06CC\u0627\u06C1", "OT", 1),
    BibleBook(32, "Jonah", "\u06CC\u064F\u0648\u0646\u0627\u06C1", "OT", 4),
    BibleBook(33, "Micah", "\u0645\u06CC\u06A9\u0627\u06C1", "OT", 7),
    BibleBook(34, "Nahum", "\u0646\u0627\u062D\u064F\u0648\u0645", "OT", 3),
    BibleBook(35, "Habakkuk", "\u062D\u0628\u0642\u064F\u0651\u0648\u0642", "OT", 3),
    BibleBook(36, "Zephaniah", "\u0635\u0641\u0646\u06CC\u0627\u06C1", "OT", 3),
    BibleBook(37, "Haggai", "\u062D\u062C\u0651\u06CC", "OT", 2),
    BibleBook(38, "Zechariah", "\u0632\u06A9\u0631\u06CC\u0627\u06C1", "OT", 14),
    BibleBook(39, "Malachi", "\u0645\u0644\u0627\u06A9\u06CC", "OT", 4)
)

val newTestamentBooks = listOf(
    BibleBook(40, "Matthew", "\u0645\u062A\u0651\u06CC", "NT", 28),
    BibleBook(41, "Mark", "\u0645\u0631\u0642\u0633", "NT", 16),
    BibleBook(42, "Luke", "\u0644\u064F\u0648\u0642\u0627", "NT", 24),
    BibleBook(43, "John", "\u06CC\u064F\u0648\u062D\u0646\u0651\u0627", "NT", 21),
    BibleBook(44, "Acts", "\u0627\u0639\u0645\u0627\u0644", "NT", 28),
    BibleBook(45, "Romans", "\u0631\u0648\u0645\u06CC\u0648\u06BA", "NT", 16),
    BibleBook(46, "1 Corinthians", "\u06F1-\u06A9\u064F\u0631\u0646\u062A\u06BE\u06CC\u0648\u06BA", "NT", 16),
    BibleBook(47, "2 Corinthians", "\u06F2-\u06A9\u064F\u0631\u0646\u062A\u06BE\u06CC\u0648\u06BA", "NT", 13),
    BibleBook(48, "Galatians", "\u06AF\u0644\u062A\u06CC\u0648\u06BA", "NT", 6),
    BibleBook(49, "Ephesians", "\u0627\u0650\u0641\u0633\u06CC\u0648\u06BA", "NT", 6),
    BibleBook(50, "Philippians", "\u0641\u0650\u0644\u067E\u0651\u06CC\u0648\u06BA", "NT", 4),
    BibleBook(51, "Colossians", "\u06A9\u064F\u0644\u0633\u0651\u06CC\u0648\u06BA", "NT", 4),
    BibleBook(52, "1 Thessalonians", "\u06F1-\u062A\u06BE\u0633\u0651\u0644\u064F\u0646\u06CC\u06A9\u06CC\u0648\u06BA", "NT", 5),
    BibleBook(53, "2 Thessalonians", "\u06F2-\u062A\u06BE\u0633\u0651\u0644\u064F\u0646\u06CC\u06A9\u06CC\u0648\u06BA", "NT", 3),
    BibleBook(54, "1 Timothy", "\u06F1-\u062A\u06CC\u0645\u064F\u062A\u06BE\u06CC\u064F\u0633", "NT", 6),
    BibleBook(55, "2 Timothy", "\u06F2-\u062A\u06CC\u0645\u064F\u062A\u06BE\u06CC\u064F\u0633", "NT", 4),
    BibleBook(56, "Titus", "\u0637\u0650\u0637\u064F\u0633", "NT", 3),
    BibleBook(57, "Philemon", "\u0641\u0650\u0644\u06CC\u0645\u0648\u0646", "NT", 1),
    BibleBook(58, "Hebrews", "\u0639\u0628\u0631\u0627\u0646\u06CC\u0648\u06BA", "NT", 13),
    BibleBook(59, "James", "\u06CC\u0639\u0642\u064F\u0648\u0628", "NT", 5),
    BibleBook(60, "1 Peter", "\u06F1-\u067E\u0637\u0631\u0633", "NT", 5),
    BibleBook(61, "2 Peter", "\u06F2-\u067E\u0637\u0631\u0633", "NT", 3),
    BibleBook(62, "1 John", "\u06F1-\u06CC\u064F\u0648\u062D\u0646\u0651\u0627", "NT", 5),
    BibleBook(63, "2 John", "\u06F2-\u06CC\u064F\u0648\u062D\u0646\u0651\u0627", "NT", 1),
    BibleBook(64, "3 John", "\u06F3-\u06CC\u064F\u0648\u062D\u0646\u0651\u0627", "NT", 1),
    BibleBook(65, "Jude", "\u06CC\u06C1\u064F\u0648\u062F\u0627\u06C1", "NT", 1),
    BibleBook(66, "Revelation", "\u0645\u06A9\u0627\u0634\u0641\u06C1", "NT", 22)
)

val allBibleBooks = oldTestamentBooks + newTestamentBooks

suspend fun fetchBibleChapter(book: String, chapter: Int, language: BibleLanguage = BibleLanguage.ENGLISH): List<BibleVerse> =
    BibleStorage.getChapter(book, chapter, language)

data class BibleSearchResult(
    val book: BibleBook, val chapter: Int,
    val verse: BibleVerse, val language: BibleLanguage
)

suspend fun searchBibleVerses(query: String, language: BibleLanguage): List<BibleSearchResult> {
    if (query.length < 2) return emptyList()
    return withContext(Dispatchers.IO) {
        val results = mutableListOf<BibleSearchResult>()
        // Search both English and Urdu Bibles
        for (lang in listOf(BibleLanguage.ENGLISH, BibleLanguage.URDU)) {
            for (book in allBibleBooks) {
                try {
                    val bookData = BibleStorage.loadBookFromAssets(book.name, lang)
                    bookData?.chapters?.forEach { chapter ->
                        chapter.verses.forEach { verse ->
                            // Use case-insensitive contains for both English and Urdu
                            if (verse.text.contains(query, ignoreCase = true)) {
                                results.add(BibleSearchResult(book, chapter.chapter, verse, lang))
                            }
                        }
                    }
                } catch (_: Exception) {}
                if (results.size >= 100) return@withContext results.take(100)
            }
        }
        results
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun BibleScreen(onBack: () -> Unit) {
    var selectedBook by remember { mutableStateOf<BibleBook?>(null) }
    var selectedChapter by remember { mutableStateOf<Int?>(null) }
    var verses by remember { mutableStateOf<List<BibleVerse>>(emptyList()) }
    var isLoading by remember { mutableStateOf(false) }
    var showBookSelector by remember { mutableStateOf(true) }
    var selectedTestament by remember { mutableStateOf("OT") }
    var fontSize by remember { mutableStateOf(16f) }
    var selectedLanguage by remember { mutableStateOf(BibleLanguage.ENGLISH) }
    var isSearching by remember { mutableStateOf(false) }
    var searchQuery by remember { mutableStateOf("") }
    var searchResults by remember { mutableStateOf<List<BibleSearchResult>>(emptyList()) }
    var isSearchLoading by remember { mutableStateOf(false) }

    LaunchedEffect(selectedBook, selectedChapter, selectedLanguage) {
        if (selectedBook != null && selectedChapter != null) {
            isLoading = true
            verses = fetchBibleChapter(selectedBook!!.name, selectedChapter!!, selectedLanguage)
            isLoading = false
            showBookSelector = false
        }
    }

    LaunchedEffect(searchQuery, selectedLanguage) {
        if (searchQuery.length >= 2) {
            isSearchLoading = true
            delay(300)
            searchResults = searchBibleVerses(searchQuery, selectedLanguage)
            isSearchLoading = false
        } else { searchResults = emptyList() }
    }

    BackHandlerEffect(enabled = isSearching || !showBookSelector || selectedBook != null) {
        when {
            isSearching -> { isSearching = false; searchQuery = ""; searchResults = emptyList() }
            !showBookSelector && selectedChapter != null -> { selectedChapter = null; showBookSelector = true }
            selectedBook != null && selectedChapter == null -> { selectedBook = null }
            else -> onBack()
        }
    }

    Scaffold(
        containerColor = MaterialTheme.colorScheme.background,
        topBar = {
            TopAppBar(
                title = {
                    if (isSearching) {
                        OutlinedTextField(
                            value = searchQuery, onValueChange = { searchQuery = it },
                            placeholder = { Text(if (selectedLanguage == BibleLanguage.URDU) "\u0622\u06CC\u0627\u062A \u062A\u0644\u0627\u0634 \u06A9\u0631\u06CC\u06BA..." else "Search verses...") },
                            singleLine = true, modifier = Modifier.fillMaxWidth(),
                            colors = OutlinedTextFieldDefaults.colors(
                                focusedBorderColor = MaterialTheme.colorScheme.primary,
                                unfocusedBorderColor = Color.Transparent
                            ),
                            shape = RoundedCornerShape(12.dp)
                        )
                    } else {
                        Column {
                            Text(
                                if (selectedBook != null && selectedChapter != null)
                                    "${selectedBook!!.getDisplayName(selectedLanguage)} $selectedChapter"
                                else if (selectedBook != null)
                                    if (selectedLanguage == BibleLanguage.URDU) "\u0628\u0627\u0628 \u0645\u0646\u062A\u062E\u0628 \u06A9\u0631\u06CC\u06BA" else "Select Chapter"
                                else if (selectedLanguage == BibleLanguage.URDU) "\u0628\u0627\u0626\u0628\u0644" else "Bible",
                                style = MaterialTheme.typography.titleLarge
                            )
                            if (selectedBook != null && selectedChapter != null) {
                                Text(
                                    if (selectedLanguage == BibleLanguage.URDU) "${verses.size} \u0622\u06CC\u0627\u062A" else "${verses.size} verses",
                                    style = MaterialTheme.typography.bodySmall,
                                    color = MaterialTheme.colorScheme.onSurfaceVariant
                                )
                            }
                        }
                    }
                },
                navigationIcon = {
                    IconButton(onClick = {
                        when {
                            isSearching -> { isSearching = false; searchQuery = ""; searchResults = emptyList() }
                            !showBookSelector && selectedChapter != null -> { selectedChapter = null; showBookSelector = true }
                            selectedBook != null && selectedChapter == null -> { selectedBook = null }
                            else -> onBack()
                        }
                    }) { Icon(Icons.AutoMirrored.Rounded.ArrowBack, contentDescription = "Back") }
                },
                actions = {
                    if (!isSearching) {
                        IconButton(onClick = { isSearching = true }) { Icon(Icons.Rounded.Search, contentDescription = "Search") }
                    }
                    Surface(
                        onClick = { selectedLanguage = if (selectedLanguage == BibleLanguage.ENGLISH) BibleLanguage.URDU else BibleLanguage.ENGLISH },
                        shape = RoundedCornerShape(8.dp), color = MaterialTheme.colorScheme.primaryContainer
                    ) {
                        Text(
                            text = if (selectedLanguage == BibleLanguage.ENGLISH) "\u0627\u064F\u0631\u062F\u064F\u0648" else "ENG",
                            modifier = Modifier.padding(horizontal = 12.dp, vertical = 6.dp),
                            style = MaterialTheme.typography.labelMedium, fontWeight = FontWeight.Bold,
                            color = MaterialTheme.colorScheme.onPrimaryContainer
                        )
                    }
                    Spacer(modifier = Modifier.width(8.dp))
                    if (!showBookSelector && verses.isNotEmpty() && !isSearching) {
                        IconButton(onClick = { if (fontSize > 12f) fontSize -= 2f }) { Text("A\u2212", fontWeight = FontWeight.Bold) }
                        IconButton(onClick = { if (fontSize < 32f) fontSize += 2f }) { Text("A+", fontWeight = FontWeight.Bold) }
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(containerColor = Color.Transparent)
            )
        }
    ) { padding ->
        Box(modifier = Modifier.fillMaxSize().padding(padding)) {
            when {
                isSearching -> BibleSearchResultsView(searchQuery, searchResults, isSearchLoading, selectedLanguage) { result ->
                    selectedBook = result.book; selectedChapter = result.chapter
                    isSearching = false; searchQuery = ""; searchResults = emptyList()
                }
                showBookSelector && selectedBook == null -> BibleBookSelector(selectedTestament, { selectedTestament = it }, { selectedBook = it }, selectedLanguage)
                showBookSelector && selectedBook != null && selectedChapter == null -> BibleChapterSelector(selectedBook!!, { selectedChapter = it }, selectedLanguage)
                isLoading -> Box(Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                    Column(horizontalAlignment = Alignment.CenterHorizontally) {
                        CircularProgressIndicator()
                        Spacer(Modifier.height(16.dp))
                        Text("Loading...", style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)
                    }
                }
                verses.isNotEmpty() -> BibleContentView(selectedBook!!, selectedChapter!!, verses, fontSize, selectedLanguage,
                    onPreviousChapter = { if (selectedChapter!! > 1) selectedChapter = selectedChapter!! - 1 },
                    onNextChapter = { if (selectedChapter!! < selectedBook!!.chapters) selectedChapter = selectedChapter!! + 1 })
                else -> Box(Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                    Column(horizontalAlignment = Alignment.CenterHorizontally, modifier = Modifier.padding(24.dp)) {
                        Text("Chapter Not Available", style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.SemiBold)
                        Spacer(Modifier.height(8.dp))
                        Text("This chapter is not yet available offline.", style = MaterialTheme.typography.bodyMedium, textAlign = TextAlign.Center, color = MaterialTheme.colorScheme.onSurfaceVariant)
                        Spacer(Modifier.height(20.dp))
                        Button(onClick = { selectedChapter = null; showBookSelector = true }, shape = RoundedCornerShape(12.dp)) { Text("Select Another Chapter") }
                    }
                }
            }
        }
    }
}

@Composable
fun BibleBookSelector(selectedTestament: String, onTestamentChange: (String) -> Unit, onBookSelect: (BibleBook) -> Unit, language: BibleLanguage = BibleLanguage.ENGLISH) {
    val books = if (selectedTestament == "OT") oldTestamentBooks else newTestamentBooks
    val isUrdu = language == BibleLanguage.URDU
    CompositionLocalProvider(LocalLayoutDirection provides if (isUrdu) LayoutDirection.Rtl else LayoutDirection.Ltr) {
        Column(modifier = Modifier.fillMaxSize()) {
            Row(
                modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp, vertical = 10.dp),
                horizontalArrangement = Arrangement.spacedBy(12.dp)
            ) {
                TestamentTab(if (isUrdu) "\u067E\u064F\u0631\u0627\u0646\u0627 \u0639\u06C1\u062F \u0646\u0627\u0645\u06C1" else "Old Testament", selectedTestament == "OT", { onTestamentChange("OT") }, Modifier.weight(1f))
                TestamentTab(if (isUrdu) "\u0646\u06CC\u0627 \u0639\u06C1\u062F \u0646\u0627\u0645\u06C1" else "New Testament", selectedTestament == "NT", { onTestamentChange("NT") }, Modifier.weight(1f))
            }
            val screenWidth = rememberScreenWidthDp()
            val columns = when { screenWidth >= 840 -> 4; screenWidth >= 600 -> 3; else -> 2 }
            LazyVerticalGrid(
                columns = GridCells.Fixed(columns),
                modifier = Modifier.fillMaxSize(),
                contentPadding = PaddingValues(horizontal = 16.dp, vertical = 12.dp),
                horizontalArrangement = Arrangement.spacedBy(12.dp),
                verticalArrangement = Arrangement.spacedBy(12.dp)
            ) {
                items(books.size, key = { books[it].name }) { index ->
                    BibleBookCard(books[index], { onBookSelect(books[index]) }, language)
                }
            }
        }
    }
}

@Composable
fun TestamentTab(title: String, selected: Boolean, onClick: () -> Unit, modifier: Modifier = Modifier) {
    Surface(
        onClick = onClick,
        modifier = modifier.height(46.dp),
        shape = RoundedCornerShape(12.dp),
        color = if (selected) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.surfaceVariant,
        shadowElevation = if (selected) 2.dp else 0.dp
    ) {
        Box(contentAlignment = Alignment.Center) {
            Text(
                title,
                style = MaterialTheme.typography.labelLarge,
                color = if (selected) Color.White else MaterialTheme.colorScheme.onSurfaceVariant,
                fontWeight = if (selected) FontWeight.Bold else FontWeight.Medium
            )
        }
    }
}

@Composable
fun BibleBookCard(book: BibleBook, onClick: () -> Unit, language: BibleLanguage = BibleLanguage.ENGLISH) {
    val isUrdu = language == BibleLanguage.URDU
    Card(
        onClick = onClick,
        shape = RoundedCornerShape(14.dp),
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface),
        elevation = CardDefaults.cardElevation(defaultElevation = 1.dp)
    ) {
        CompositionLocalProvider(LocalLayoutDirection provides if (isUrdu) LayoutDirection.Rtl else LayoutDirection.Ltr) {
            Column(modifier = Modifier.fillMaxWidth().padding(14.dp)) {
                Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.End) {
                    Surface(shape = RoundedCornerShape(8.dp), color = MaterialTheme.colorScheme.primaryContainer.copy(alpha = 0.5f)) {
                        Text(
                            "${book.chapters}",
                            style = MaterialTheme.typography.labelMedium,
                            fontWeight = FontWeight.Bold,
                            color = MaterialTheme.colorScheme.primary,
                            modifier = Modifier.padding(horizontal = 8.dp, vertical = 3.dp)
                        )
                    }
                }
                Spacer(Modifier.height(10.dp))
                Text(
                    book.getDisplayName(language),
                    style = MaterialTheme.typography.titleSmall,
                    fontWeight = FontWeight.Bold,
                    maxLines = 2,
                    overflow = TextOverflow.Ellipsis,
                    color = MaterialTheme.colorScheme.onSurface
                )
                Spacer(Modifier.height(4.dp))
                Text(
                    if (isUrdu) "${book.chapters} \u0627\u0628\u0648\u0627\u0628" else "${book.chapters} ch.",
                    style = MaterialTheme.typography.labelSmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }
        }
    }
}

@Composable
fun BibleChapterSelector(book: BibleBook, onChapterSelect: (Int) -> Unit, language: BibleLanguage = BibleLanguage.ENGLISH) {
    val screenWidth = rememberScreenWidthDp()
    val columns = when { screenWidth >= 840 -> 10; screenWidth >= 600 -> 8; else -> 6 }
    val isUrdu = language == BibleLanguage.URDU
    CompositionLocalProvider(LocalLayoutDirection provides if (isUrdu) LayoutDirection.Rtl else LayoutDirection.Ltr) {
        Column(modifier = Modifier.fillMaxSize()) {
            Surface(
                modifier = Modifier.fillMaxWidth(),
                color = MaterialTheme.colorScheme.primaryContainer.copy(alpha = 0.6f),
                tonalElevation = 2.dp
            ) {
                Column(modifier = Modifier.fillMaxWidth().padding(horizontal = 24.dp, vertical = 20.dp)) {
                    Text(
                        book.getDisplayName(language),
                        style = MaterialTheme.typography.headlineSmall,
                        fontWeight = FontWeight.Bold,
                        color = MaterialTheme.colorScheme.onPrimaryContainer
                    )
                    Spacer(Modifier.height(6.dp))
                    Text(
                        if (isUrdu) "\u0628\u0627\u0628 \u0645\u0646\u062A\u062E\u0628 \u06A9\u0631\u06CC\u06BA" else "Select a Chapter",
                        style = MaterialTheme.typography.bodyMedium,
                        color = MaterialTheme.colorScheme.onPrimaryContainer.copy(alpha = 0.7f)
                    )
                }
            }
            LazyVerticalGrid(
                columns = GridCells.Fixed(columns),
                modifier = Modifier.fillMaxSize(),
                contentPadding = PaddingValues(16.dp),
                horizontalArrangement = Arrangement.spacedBy(10.dp),
                verticalArrangement = Arrangement.spacedBy(10.dp)
            ) {
                items(book.chapters, key = { it }) { index ->
                    Card(
                        onClick = { onChapterSelect(index + 1) },
                        modifier = Modifier.aspectRatio(1f),
                        shape = RoundedCornerShape(12.dp),
                        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant),
                        elevation = CardDefaults.cardElevation(defaultElevation = 1.dp)
                    ) {
                        Box(contentAlignment = Alignment.Center, modifier = Modifier.fillMaxSize()) {
                            Text(
                                "${index + 1}",
                                style = MaterialTheme.typography.titleMedium,
                                fontWeight = FontWeight.Bold,
                                color = MaterialTheme.colorScheme.primary
                            )
                        }
                    }
                }
            }
        }
    }
}

@Composable
fun BibleSearchResultsView(query: String, results: List<BibleSearchResult>, isLoading: Boolean, language: BibleLanguage, onResultClick: (BibleSearchResult) -> Unit) {
    val isUrdu = language == BibleLanguage.URDU
    val urduFontFamily = LocalUrduFont.current
    Column(modifier = Modifier.fillMaxSize()) {
        if (query.isNotEmpty() && results.isNotEmpty()) {
            Surface(modifier = Modifier.fillMaxWidth(), color = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f)) {
                Text(
                    "${results.size} results found",
                    modifier = Modifier.padding(horizontal = 16.dp, vertical = 12.dp),
                    style = MaterialTheme.typography.labelLarge,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }
        }
        when {
            isLoading -> Box(Modifier.fillMaxSize(), contentAlignment = Alignment.Center) { CircularProgressIndicator() }
            results.isEmpty() && query.length >= 2 -> Box(Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                Column(horizontalAlignment = Alignment.CenterHorizontally) {
                    Text(if (isUrdu) "\u06A9\u0648\u0626\u06CC \u0622\u06CC\u062A \u0646\u06C1\u06CC\u06BA \u0645\u0644\u06CC" else "No verses found", style = MaterialTheme.typography.titleMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)
                    Spacer(Modifier.height(4.dp))
                    Text(if (isUrdu) "\u062F\u0648\u0633\u0631\u06CC \u062A\u0644\u0627\u0634 \u06A9\u0631\u06CC\u06BA" else "Try a different search term", style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.7f))
                }
            }
            query.length < 2 -> Box(Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                Text(if (isUrdu) "\u062A\u0644\u0627\u0634 \u0634\u0631\u0648\u0639 \u06A9\u0631\u06CC\u06BA" else "Start typing to search", style = MaterialTheme.typography.titleMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)
            }
            else -> LazyColumn(modifier = Modifier.fillMaxSize(), contentPadding = PaddingValues(horizontal = 16.dp, vertical = 12.dp), verticalArrangement = Arrangement.spacedBy(10.dp)) {
                items(results.size) { index ->
                    val result = results[index]
                    val resultIsUrdu = result.language == BibleLanguage.URDU
                    Card(onClick = { onResultClick(result) }, shape = RoundedCornerShape(14.dp),
                        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface),
                        elevation = CardDefaults.cardElevation(defaultElevation = 1.dp)) {
                        CompositionLocalProvider(LocalLayoutDirection provides if (resultIsUrdu) LayoutDirection.Rtl else LayoutDirection.Ltr) {
                            Column(modifier = Modifier.fillMaxWidth().padding(14.dp)) {
                                Row(horizontalArrangement = Arrangement.spacedBy(8.dp), verticalAlignment = Alignment.CenterVertically) {
                                    Surface(shape = RoundedCornerShape(8.dp), color = MaterialTheme.colorScheme.primaryContainer) {
                                        Text(result.book.getDisplayName(result.language),
                                            style = MaterialTheme.typography.labelMedium, fontWeight = FontWeight.Bold,
                                            color = MaterialTheme.colorScheme.onPrimaryContainer, modifier = Modifier.padding(horizontal = 10.dp, vertical = 4.dp))
                                    }
                                    Text("${result.chapter}:${result.verse.verse}", style = MaterialTheme.typography.labelLarge, fontWeight = FontWeight.SemiBold, color = MaterialTheme.colorScheme.primary)
                                    Spacer(Modifier.weight(1f))
                                    Surface(shape = RoundedCornerShape(6.dp), color = MaterialTheme.colorScheme.secondaryContainer) {
                                        Text(if (resultIsUrdu) "\u0627\u0631\u062F\u0648" else "ENG",
                                            style = MaterialTheme.typography.labelSmall, fontWeight = FontWeight.Bold,
                                            color = MaterialTheme.colorScheme.onSecondaryContainer, modifier = Modifier.padding(horizontal = 8.dp, vertical = 3.dp))
                                    }
                                }
                                Spacer(Modifier.height(10.dp))
                                Text(result.verse.text, style = MaterialTheme.typography.bodyMedium.copy(
                                    fontFamily = if (resultIsUrdu) urduFontFamily else FontFamily.Default,
                                    lineHeight = if (resultIsUrdu) 28.sp else 22.sp),
                                    color = MaterialTheme.colorScheme.onSurface, maxLines = 4, overflow = TextOverflow.Ellipsis)
                            }
                        }
                    }
                }
            }
        }
    }
}

@Composable
fun BibleContentView(book: BibleBook, chapter: Int, verses: List<BibleVerse>, fontSize: Float,
    language: BibleLanguage = BibleLanguage.ENGLISH, onPreviousChapter: () -> Unit, onNextChapter: () -> Unit) {
    val screenWidth = rememberScreenWidthDp()
    val horizontalPadding = when { screenWidth >= 840 -> 120.dp; screenWidth >= 600 -> 60.dp; else -> 20.dp }
    val isUrdu = language == BibleLanguage.URDU
    val adjustedFontSize = if (isUrdu) fontSize + 2 else fontSize
    val lineHeightMultiplier = if (isUrdu) 2.0f else 1.7f
    val urduFontFamily = LocalUrduFont.current
    val listState = rememberLazyListState()
    val coroutineScope = rememberCoroutineScope()
    val showScrollToTop = remember { derivedStateOf { listState.firstVisibleItemIndex > 5 } }

    Box(modifier = Modifier.fillMaxSize()) {
        Column(modifier = Modifier.fillMaxSize()) {
            val progress = remember { derivedStateOf { if (verses.isEmpty()) 0f else (listState.firstVisibleItemIndex.toFloat() / verses.size.toFloat()).coerceIn(0f, 1f) } }
            LinearProgressIndicator(progress = { progress.value }, modifier = Modifier.fillMaxWidth().height(3.dp), color = MaterialTheme.colorScheme.primary, trackColor = MaterialTheme.colorScheme.surfaceVariant)
            Surface(modifier = Modifier.fillMaxWidth(), color = MaterialTheme.colorScheme.primaryContainer.copy(alpha = 0.25f), tonalElevation = 1.dp) {
                CompositionLocalProvider(LocalLayoutDirection provides if (isUrdu) LayoutDirection.Rtl else LayoutDirection.Ltr) {
                    Column(modifier = Modifier.fillMaxWidth().padding(horizontal = horizontalPadding, vertical = 14.dp)) {
                        Text(book.getDisplayName(language), style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.onSurface)
                        Spacer(Modifier.height(2.dp))
                        Text(if (isUrdu) "\u0628\u0627\u0628 $chapter \u2014 ${verses.size} \u0622\u06CC\u0627\u062A" else "Chapter $chapter \u2014 ${verses.size} verses",
                            style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.primary)
                    }
                }
            }
            LazyColumn(state = listState, modifier = Modifier.weight(1f).fillMaxWidth(),
                contentPadding = PaddingValues(start = horizontalPadding, end = horizontalPadding, top = 16.dp, bottom = 100.dp)) {
                items(verses.size) { index ->
                    val verse = verses[index]
                    CompositionLocalProvider(LocalLayoutDirection provides if (isUrdu) LayoutDirection.Rtl else LayoutDirection.Ltr) {
                        Row(modifier = Modifier.fillMaxWidth().padding(top = if (index == 0) 0.dp else if (isUrdu) 10.dp else 6.dp),
                            horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                            // Verse number with subtle background
                            Surface(
                                shape = RoundedCornerShape(6.dp),
                                color = MaterialTheme.colorScheme.primaryContainer.copy(alpha = 0.3f),
                                modifier = Modifier.padding(top = 4.dp)
                            ) {
                                Text(
                                    "${verse.verse}",
                                    style = MaterialTheme.typography.labelSmall.copy(fontSize = (adjustedFontSize - 6).sp),
                                    color = MaterialTheme.colorScheme.primary,
                                    fontWeight = FontWeight.Bold,
                                    modifier = Modifier.padding(horizontal = 5.dp, vertical = 2.dp)
                                )
                            }
                            Text(verse.text, style = MaterialTheme.typography.bodyLarge.copy(
                                fontSize = adjustedFontSize.sp, lineHeight = (adjustedFontSize * lineHeightMultiplier).sp,
                                fontFamily = if (isUrdu) urduFontFamily else FontFamily.Default),
                                color = MaterialTheme.colorScheme.onBackground, modifier = Modifier.weight(1f))
                        }
                    }
                }
            }
        }
        // Floating Navigation Bar
        Surface(modifier = Modifier.align(Alignment.BottomCenter).fillMaxWidth().padding(horizontal = 16.dp, vertical = 12.dp),
            shape = RoundedCornerShape(16.dp), color = MaterialTheme.colorScheme.surface, shadowElevation = 8.dp, tonalElevation = 3.dp) {
            Row(modifier = Modifier.fillMaxWidth().padding(10.dp), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                FilledTonalButton(onClick = onPreviousChapter, enabled = chapter > 1, shape = RoundedCornerShape(12.dp), modifier = Modifier.weight(1f)) {
                    Icon(Icons.AutoMirrored.Rounded.ArrowBack, contentDescription = "Previous", modifier = Modifier.size(18.dp))
                    Spacer(Modifier.width(4.dp)); Text(if (language == BibleLanguage.URDU) "\u067E\u0686\u06BE\u0644\u0627" else "Prev", style = MaterialTheme.typography.labelLarge)
                }
                Surface(shape = RoundedCornerShape(10.dp), color = MaterialTheme.colorScheme.primaryContainer, modifier = Modifier.padding(horizontal = 10.dp)) {
                    Text("$chapter / ${book.chapters}", style = MaterialTheme.typography.labelLarge, color = MaterialTheme.colorScheme.onPrimaryContainer,
                        fontWeight = FontWeight.Bold, modifier = Modifier.padding(horizontal = 14.dp, vertical = 8.dp))
                }
                Button(onClick = onNextChapter, enabled = chapter < book.chapters, shape = RoundedCornerShape(12.dp), modifier = Modifier.weight(1f)) {
                    Text(if (language == BibleLanguage.URDU) "\u0627\u06AF\u0644\u0627" else "Next", style = MaterialTheme.typography.labelLarge)
                    Spacer(Modifier.width(4.dp)); Icon(Icons.AutoMirrored.Rounded.ArrowForward, contentDescription = "Next", modifier = Modifier.size(18.dp))
                }
            }
        }
        if (showScrollToTop.value) {
            SmallFloatingActionButton(onClick = { coroutineScope.launch { listState.animateScrollToItem(0) } },
                modifier = Modifier.align(Alignment.BottomEnd).padding(end = 16.dp, bottom = 88.dp),
                containerColor = MaterialTheme.colorScheme.tertiaryContainer, contentColor = MaterialTheme.colorScheme.onTertiaryContainer) {
                Icon(Icons.Rounded.KeyboardArrowUp, contentDescription = "Scroll to top")
            }
        }
    }
}

// ============ SONG DATA & DOWNLOAD ============

data class SongItem(
    val id: Int, 
    val title: String, 
    val lyrics: String, 
    val language: String,
    val category: String, 
    val indexChar: String, 
    val heading: String? = null, 
    val isPunjabi: Boolean = false,
    val isActive: Int = 1,
    val version: Long = 0L
)

fun isUrduText(text: String): Boolean = text.any { it.code in 0x0600..0x06FF }

object SongApi {
    const val BASE_URL = "https://cpa-pk.org/pages/api/songs.php"
}

private const val CACHE_FILE = "cached_songs.json"

@Serializable
data class SongRaw(
    val id: Int = 0,
    val title: String = "",
    val author: String = "",
    val category: String = "",
    val song_number: Int = 0,
    val sort_order: Int = 0,
    val is_active: Int = 1,
    val version: Long = 0L,
    val updated_at: String = "",
    val lyrics: String = ""
)

@Serializable
data class VersionResponse(
    val success: Boolean = false,
    val version: Long = 0L,
    val total: Int = 0
)

@Serializable
data class ExportResponse(
    val success: Boolean = false,
    val version: Long = 0L,
    val total: Int = 0,
    val songs: SongsGrouped = SongsGrouped()
)

@Serializable
data class SongsGrouped(
    val zaboor: List<SongRaw> = emptyList(),
    val geet: List<SongRaw> = emptyList(),
    val english: List<SongRaw> = emptyList()
)

@Serializable
data class IncrementalResponse(
    val success: Boolean = false,
    val version: Long = 0L,
    val changes: Int = 0,
    val songs: List<SongRaw> = emptyList()
)

private val songJsonParser = Json { ignoreUnknownKeys = true; isLenient = true }
private val httpClient = HttpClient()

suspend fun loadSongsAsync(): List<SongItem> = withContext(Dispatchers.Default) {
    // Load from cache immediately for fast startup
    val cachedSongs = loadFromCache()
    
    // Try to sync with API in background
    try {
        val storedVersion = readSongVersion()
        
        // Check if update available
        val versionCheck = httpClient.get("${SongApi.BASE_URL}?version=1") {
            headers {
                append("Cache-Control", "no-cache, no-store")
                append("Pragma", "no-cache")
            }
        }
        
        if (versionCheck.status.isSuccess()) {
            val versionData: VersionResponse = songJsonParser.decodeFromString(versionCheck.bodyAsText())
            platformLog("CPA_SONGS", "API version: ${versionData.version}, Stored: $storedVersion")
            
            if (versionData.version != storedVersion || storedVersion == 0L) {
                // Need to sync - choose full export or incremental
                val updatedSongs = if (storedVersion == 0L || cachedSongs.isEmpty()) {
                    // First install - full export
                    platformLog("CPA_SONGS", "First install - downloading full export")
                    downloadFullExport()
                } else {
                    // Incremental sync
                    platformLog("CPA_SONGS", "Syncing changes since $storedVersion")
                    syncIncremental(storedVersion, cachedSongs)
                }
                
                if (updatedSongs.isNotEmpty()) {
                    // Save to cache
                    try {
                        val songsRaw = updatedSongs.map { it.toSongRaw() }
                        val cacheJson = songJsonParser.encodeToString(kotlinx.serialization.builtins.ListSerializer(SongRaw.serializer()), songsRaw)
                        writeCacheFile(CACHE_FILE, cacheJson)
                        writeSongVersion(versionData.version)
                        platformLog("CPA_SONGS", "Synced ${updatedSongs.size} songs, version ${versionData.version}")
                    } catch (e: Exception) {
                        platformLog("CPA_SONGS", "Cache save failed: ${e.message}")
                    }
                    return@withContext updatedSongs
                }
            } else {
                platformLog("CPA_SONGS", "Cache is up to date (v${storedVersion})")
            }
        }
    } catch (e: Exception) {
        platformLog("CPA_SONGS", "API sync failed: ${e.message}")
    }
    
    // Return cached songs if sync failed or cache is current
    if (cachedSongs.isNotEmpty()) {
        return@withContext cachedSongs
    }
    
    // Last resort - load bundled assets
    platformLog("CPA_SONGS", "Loading from bundled assets")
    loadFromBundledAssets()
}

private suspend fun downloadFullExport(): List<SongItem> {
    return try {
        val response = httpClient.get("${SongApi.BASE_URL}?export=1") {
            headers {
                append("Cache-Control", "no-cache, no-store")
                append("Pragma", "no-cache")
            }
        }
        if (response.status.isSuccess()) {
            val exportData: ExportResponse = songJsonParser.decodeFromString(response.bodyAsText())
            val allRaw = mutableListOf<SongRaw>()
            allRaw += exportData.songs.zaboor
            allRaw += exportData.songs.geet
            allRaw += exportData.songs.english
            allRaw.filter { it.is_active == 1 }.map { it.toSongItem() }
        } else emptyList()
    } catch (e: Exception) {
        platformLog("CPA_SONGS", "Full export failed: ${e.message}")
        emptyList()
    }
}

private suspend fun syncIncremental(storedVersion: Long, cachedSongs: List<SongItem>): List<SongItem> {
    return try {
        val response = httpClient.get("${SongApi.BASE_URL}?since=$storedVersion") {
            headers {
                append("Cache-Control", "no-cache, no-store")
                append("Pragma", "no-cache")
            }
        }
        if (response.status.isSuccess()) {
            val incrementalData: IncrementalResponse = songJsonParser.decodeFromString(response.bodyAsText())
            platformLog("CPA_SONGS", "Incremental changes: ${incrementalData.changes}")
            
            // Apply changes to cached list
            val songMap = cachedSongs.associateBy { it.id }.toMutableMap()
            for (change in incrementalData.songs) {
                if (change.is_active == 1) {
                    // Update or insert
                    songMap[change.id] = change.toSongItem()
                } else {
                    // Delete
                    songMap.remove(change.id)
                }
            }
            songMap.values.toList().sortedBy { it.title }
        } else cachedSongs
    } catch (e: Exception) {
        platformLog("CPA_SONGS", "Incremental sync failed: ${e.message}")
        cachedSongs
    }
}

private suspend fun loadFromCache(): List<SongItem> {
    return try {
        val cacheJson = readCacheFile(CACHE_FILE)
        if (!cacheJson.isNullOrEmpty()) {
            val rawSongs: List<SongRaw> = songJsonParser.decodeFromString(cacheJson)
            rawSongs.filter { it.is_active == 1 }.map { it.toSongItem() }
        } else emptyList()
    } catch (e: Exception) {
        platformLog("CPA_SONGS", "Cache load failed: ${e.message}")
        emptyList()
    }
}

private suspend fun loadFromBundledAssets(): List<SongItem> {
    return try {
        val urduJson = readAssetFile("urdusongs.json") ?: ""
        val englishJson = readAssetFile("englishsongs.json") ?: ""
        val allSongs = mutableListOf<SongItem>()
        
        // Parse old-format bundled assets (legacy fallback)
        if (urduJson.isNotEmpty()) {
            allSongs += parseJsonToSongsLegacy(urduJson, isUrdu = true)
        }
        if (englishJson.isNotEmpty()) {
            allSongs += parseJsonToSongsLegacy(englishJson, isUrdu = false)
        }
        
        allSongs.distinctBy { it.title }.sortedBy { it.title }
    } catch (e: Exception) {
        platformLog("CPA_SONGS", "Asset load failed: ${e.message}")
        emptyList()
    }
}

// Legacy parser for old bundled assets (urdusongs.json, englishsongs.json)
@Serializable
private data class SongRawLegacy(
    val title: String = "", 
    val content: String = "", 
    val category: String = "Song",
    val language: String = "", 
    @SerialName("section_label") val sectionLabel: String? = null,
    val heading: String? = null
)

private fun parseJsonToSongsLegacy(jsonString: String, isUrdu: Boolean): List<SongItem> {
    return try {
        val rawSongs: List<SongRawLegacy> = songJsonParser.decodeFromString(jsonString)
        rawSongs.mapIndexed { index, raw ->
            val lyrics = raw.content
            val categoryRaw = raw.category
            val language = raw.language.ifEmpty { if (isUrduText(lyrics)) "Urdu" else "English" }
            val isPsalm = categoryRaw.contains("psalms", ignoreCase = true) || categoryRaw.equals("Psalm", ignoreCase = true)
            SongItem(
                id = (if (isUrdu) 0 else 5000) + index,
                title = raw.title,
                lyrics = lyrics,
                language = language,
                category = if (isPsalm) "Psalm" else "Song",
                indexChar = raw.sectionLabel ?: (raw.title.firstOrNull()?.toString()?.uppercase() ?: "#"),
                heading = raw.heading,
                isPunjabi = isUrdu && (isPsalm || lyrics.contains("\u0633\u0627\u0688\u0627") || lyrics.contains("\u0633\u0627\u0646\u0648\u06BA"))
            )
        }
    } catch (e: Exception) {
        platformLog("CPA_SONGS", "Legacy JSON parse failed: ${e.message}")
        emptyList()
    }
}

// Convert API SongRaw to runtime SongItem
private fun SongRaw.toSongItem(): SongItem {
    val isUrdu = isUrduText(lyrics) || category in listOf("zaboor", "geet")
    val normalizedCategory = when (category.lowercase()) {
        "zaboor" -> "Psalm"
        "geet" -> "Song"
        "english" -> "Song"
        else -> "Song"
    }
    val normalizedLanguage = when (category.lowercase()) {
        "zaboor", "geet" -> "Urdu"
        "english" -> "English"
        else -> if (isUrduText(lyrics)) "Urdu" else "English"
    }
    return SongItem(
        id = id,
        title = title,
        lyrics = lyrics,
        language = normalizedLanguage,
        category = normalizedCategory,
        indexChar = title.firstOrNull()?.toString()?.uppercase() ?: "#",
        heading = author.takeIf { it.isNotEmpty() },
        isPunjabi = isUrdu && (lyrics.contains("\u0633\u0627\u0688\u0627") || lyrics.contains("\u0633\u0627\u0646\u0648\u06BA")),
        isActive = is_active,
        version = version
    )
}

// Convert SongItem back to SongRaw for caching
private fun SongItem.toSongRaw(): SongRaw {
    val apiCategory = when {
        category == "Psalm" && language == "Urdu" -> "zaboor"
        category == "Song" && language == "Urdu" -> "geet"
        language == "English" -> "english"
        else -> "geet"
    }
    return SongRaw(
        id = id,
        title = title,
        author = heading ?: "",
        category = apiCategory,
        song_number = 0,
        sort_order = 0,
        is_active = isActive,
        version = version,
        updated_at = "",
        lyrics = lyrics
    )
}

// ============ SONG BOOK UI ============

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SongBookApp(onBack: () -> Unit = {}) {
    var selectedSong by remember { mutableStateOf<SongItem?>(null) }
    var selectedLetter by remember { mutableStateOf<String?>(null) }
    var selectedTab by remember { mutableIntStateOf(2) }
    var searchQuery by remember { mutableStateOf("") }
    var isSearching by remember { mutableStateOf(false) }
    var allSongs by remember { mutableStateOf<List<SongItem>>(emptyList()) }
    var isLoading by remember { mutableStateOf(true) }
    LaunchedEffect(Unit) { allSongs = loadSongsAsync(); isLoading = false }

    val filteredSongs = allSongs.filter { song ->
        val matchesTab = when (selectedTab) { 1 -> song.language.equals("English", ignoreCase = true); 2 -> song.language.equals("Urdu", ignoreCase = true) && song.category == "Song"; 3 -> song.language.equals("Urdu", ignoreCase = true) && song.category == "Psalm"; else -> true }
        val matchesSearch = searchQuery.isEmpty() || song.title.contains(searchQuery, ignoreCase = true) || (song.heading?.contains(searchQuery, ignoreCase = true) ?: false) || song.lyrics.contains(searchQuery, ignoreCase = true)
        matchesTab && matchesSearch
    }

    BackHandlerEffect(enabled = selectedSong != null || selectedLetter != null || isSearching) {
        when { selectedSong != null -> selectedSong = null; selectedLetter != null -> selectedLetter = null; isSearching -> { isSearching = false; searchQuery = "" } }
    }

    Scaffold(containerColor = MaterialTheme.colorScheme.background, topBar = {
        Column(modifier = Modifier.background(MaterialTheme.colorScheme.background).statusBarsPadding()) {
            TopAppBar(title = {
                when {
                    selectedSong != null -> {}
                    isSearching -> SongSearchBar(searchQuery, { searchQuery = it }, { searchQuery = "" })
                    selectedLetter != null -> {
                        val isUrdu = isUrduText(selectedLetter!!)
                        Text(selectedLetter!!, style = if (isUrdu) MaterialTheme.typography.headlineMedium.copy(fontFamily = LocalUrduFont.current, fontWeight = FontWeight.Bold) else MaterialTheme.typography.headlineMedium.copy(fontWeight = FontWeight.Bold), color = MaterialTheme.colorScheme.primary)
                    }
                    else -> Column {
                        Text("CPA", style = MaterialTheme.typography.labelMedium, color = MaterialTheme.colorScheme.primary, letterSpacing = 3.sp)
                        Text("Songs Book", style = MaterialTheme.typography.titleLarge.copy(fontWeight = FontWeight.SemiBold))
                    }
                }
            }, navigationIcon = {
                IconButton(onClick = { when { selectedSong != null -> selectedSong = null; selectedLetter != null -> selectedLetter = null; isSearching -> { isSearching = false; searchQuery = "" }; else -> onBack() } }) {
                    Icon(Icons.AutoMirrored.Rounded.ArrowBack, contentDescription = "Back", tint = MaterialTheme.colorScheme.onBackground)
                }
            }, actions = {
                if (selectedSong == null && !isSearching) IconButton(onClick = { isSearching = true }) { Icon(Icons.Rounded.Search, contentDescription = "Search", tint = MaterialTheme.colorScheme.onBackground) }
            }, colors = TopAppBarDefaults.topAppBarColors(containerColor = Color.Transparent))
            if (!isSearching && selectedSong == null && selectedLetter == null) CategoryTabs(selectedTab) { selectedTab = it }
        }
    }) { innerPadding ->
        Box(modifier = Modifier.padding(innerPadding).fillMaxSize()) {
            val songPageKey = when { selectedSong != null -> 3; isLoading -> -1; selectedLetter != null || isSearching -> 2; else -> 1 }
            AnimatedContent(targetState = songPageKey, transitionSpec = {
                if (targetState > initialState) slideInHorizontally { it } togetherWith slideOutHorizontally { -it }
                else slideInHorizontally { -it } togetherWith slideOutHorizontally { it }
            }, label = "songTransition") { page ->
                when (page) {
                    3 -> selectedSong?.let { SongDetailScreen(it) }
                    -1 -> Box(Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                        Column(horizontalAlignment = Alignment.CenterHorizontally) {
                            CircularProgressIndicator()
                            Spacer(Modifier.height(16.dp))
                            Text("Loading songs...", style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)
                        }
                    }
                    2 -> { val displayList = if (isSearching) filteredSongs else filteredSongs.filter { it.indexChar == selectedLetter }; SongListScreen(displayList) { selectedSong = it } }
                    else -> SongIndexScreen(filteredSongs.groupBy { it.indexChar }.toList().sortedBy { it.first }.associate { it.first to it.second }) { selectedLetter = it }
                }
            }
        }
    }
}

@Composable
fun SongSearchBar(query: String, onQueryChange: (String) -> Unit, onClear: () -> Unit) {
    OutlinedTextField(value = query, onValueChange = onQueryChange, placeholder = { Text("Search songs...") },
        modifier = Modifier.fillMaxWidth().height(52.dp), shape = RoundedCornerShape(16.dp),
        colors = OutlinedTextFieldDefaults.colors(focusedContainerColor = MaterialTheme.colorScheme.surfaceVariant, unfocusedContainerColor = MaterialTheme.colorScheme.surfaceVariant, focusedBorderColor = MaterialTheme.colorScheme.primary.copy(alpha = 0.5f), unfocusedBorderColor = Color.Transparent),
        trailingIcon = { if (query.isNotEmpty()) IconButton(onClick = onClear) { Icon(Icons.Rounded.Close, contentDescription = "Clear", modifier = Modifier.size(20.dp)) } },
        singleLine = true)
}

@Composable
fun CategoryTabs(selectedTab: Int, onTabSelected: (Int) -> Unit) {
    val tabs = listOf("All", "English", "Geet", "Zaboor")
    ScrollableTabRow(selectedTabIndex = selectedTab, containerColor = Color.Transparent, contentColor = MaterialTheme.colorScheme.primary, edgePadding = 16.dp, divider = {},
        indicator = { tabPositions ->
            if (selectedTab < tabPositions.size) {
                val left by animateDpAsState(tabPositions[selectedTab].left, spring(Spring.DampingRatioMediumBouncy, Spring.StiffnessMediumLow), label = "l")
                val width by animateDpAsState(tabPositions[selectedTab].width, spring(Spring.DampingRatioMediumBouncy, Spring.StiffnessMediumLow), label = "w")
                Box(Modifier.fillMaxWidth().wrapContentSize(Alignment.BottomStart).offset(x = left).width(width).height(3.dp).padding(horizontal = 24.dp).clip(RoundedCornerShape(topStart = 3.dp, topEnd = 3.dp)).background(MaterialTheme.colorScheme.primary))
            }
        }) {
        tabs.forEachIndexed { index, title ->
            val selected = selectedTab == index
            Tab(selected = selected, onClick = { onTabSelected(index) }, text = {
                Text(title, style = MaterialTheme.typography.labelLarge, fontWeight = if (selected) FontWeight.Bold else FontWeight.Medium,
                    color = if (selected) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onSurfaceVariant)
            })
        }
    }
}

@Composable
fun SongIndexScreen(grouped: Map<String, List<SongItem>>, onLetterClick: (String) -> Unit) {
    val keys = grouped.keys.toList()
    val isRtl = keys.any { isUrduText(it) }
    val screenWidth = rememberScreenWidthDp()
    val columns = when { screenWidth >= 840 -> 6; screenWidth >= 600 -> 4; else -> 3 }
    CompositionLocalProvider(LocalLayoutDirection provides if (isRtl) LayoutDirection.Rtl else LayoutDirection.Ltr) {
        LazyVerticalGrid(columns = GridCells.Fixed(columns), modifier = Modifier.fillMaxSize(), contentPadding = PaddingValues(20.dp),
            horizontalArrangement = Arrangement.spacedBy(12.dp), verticalArrangement = Arrangement.spacedBy(12.dp)) {
            items(keys.size, key = { keys[it] }) { index ->
                val char = keys[index]; val isUrdu = isUrduText(char)
                Card(onClick = { onLetterClick(char) }, modifier = Modifier.aspectRatio(1f), shape = RoundedCornerShape(18.dp),
                    colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface), elevation = CardDefaults.cardElevation(defaultElevation = 1.dp)) {
                    Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                        Column(horizontalAlignment = Alignment.CenterHorizontally) {
                            Text(char, style = if (isUrdu) MaterialTheme.typography.headlineLarge.copy(fontFamily = LocalUrduFont.current, fontSize = 32.sp) else MaterialTheme.typography.headlineLarge, color = MaterialTheme.colorScheme.primary)
                            Spacer(Modifier.height(4.dp))
                            Surface(shape = RoundedCornerShape(8.dp), color = MaterialTheme.colorScheme.primaryContainer.copy(alpha = 0.4f)) {
                                Text("${grouped[char]?.size ?: 0}", style = MaterialTheme.typography.labelSmall, fontWeight = FontWeight.Bold,
                                    color = MaterialTheme.colorScheme.primary, modifier = Modifier.padding(horizontal = 8.dp, vertical = 2.dp))
                            }
                        }
                    }
                }
            }
        }
    }
}

@Composable
fun SongListScreen(songs: List<SongItem>, onSongClick: (SongItem) -> Unit) {
    if (songs.isEmpty()) {
        Box(Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
            Column(horizontalAlignment = Alignment.CenterHorizontally) {
                Text("No songs found", style = MaterialTheme.typography.titleMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)
                Spacer(Modifier.height(4.dp))
                Text("Try a different search or category", style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.7f))
            }
        }
        return
    }
    LazyColumn(modifier = Modifier.fillMaxSize(), contentPadding = PaddingValues(vertical = 8.dp)) {
        itemsIndexed(songs, key = { _, song -> song.id }) { index, song -> SongListItem(song, index) { onSongClick(song) } }
    }
}

@Composable
fun SongListItem(song: SongItem, index: Int, onClick: () -> Unit) {
    val isUrduTitle = isUrduText(song.title)
    Card(onClick = onClick, modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp, vertical = 5.dp), shape = RoundedCornerShape(14.dp),
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface), elevation = CardDefaults.cardElevation(defaultElevation = 1.dp)) {
        CompositionLocalProvider(LocalLayoutDirection provides if (isUrduTitle) LayoutDirection.Rtl else LayoutDirection.Ltr) {
            Row(modifier = Modifier.fillMaxWidth().padding(horizontal = 14.dp, vertical = 14.dp), verticalAlignment = Alignment.CenterVertically) {
                // Number badge with gradient
                Box(
                    modifier = Modifier.size(42.dp).clip(CircleShape)
                        .background(brush = Brush.linearGradient(
                            colors = listOf(
                                MaterialTheme.colorScheme.primary.copy(alpha = 0.8f),
                                MaterialTheme.colorScheme.primary
                            )
                        )),
                    contentAlignment = Alignment.Center
                ) {
                    Text("${index + 1}", style = MaterialTheme.typography.labelLarge, color = Color.White, fontWeight = FontWeight.Bold)
                }
                Spacer(Modifier.width(14.dp))
                Column(modifier = Modifier.weight(1f)) {
                    if (song.category == "Psalm" && song.heading != null) {
                        Text(song.heading, style = MaterialTheme.typography.labelSmall.let { if (isUrduText(song.heading)) it.copy(fontFamily = LocalUrduFont.current) else it }, color = MaterialTheme.colorScheme.primary.copy(alpha = 0.7f), maxLines = 1, overflow = TextOverflow.Ellipsis)
                        Spacer(Modifier.height(2.dp))
                    }
                    Text(song.title, style = if (isUrduTitle) MaterialTheme.typography.titleSmall.copy(fontFamily = LocalUrduFont.current, fontSize = 17.sp, lineHeight = 26.sp) else MaterialTheme.typography.titleSmall.copy(fontSize = 15.sp),
                        color = MaterialTheme.colorScheme.onSurface, maxLines = 2, overflow = TextOverflow.Ellipsis)
                    Spacer(Modifier.height(4.dp))
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Surface(shape = RoundedCornerShape(6.dp), color = if (song.category == "Psalm") MaterialTheme.colorScheme.tertiaryContainer else MaterialTheme.colorScheme.secondaryContainer) {
                            Text(song.category, modifier = Modifier.padding(horizontal = 7.dp, vertical = 2.dp), style = MaterialTheme.typography.labelSmall.copy(fontSize = 10.sp),
                                color = if (song.category == "Psalm") MaterialTheme.colorScheme.onTertiaryContainer else MaterialTheme.colorScheme.onSecondaryContainer)
                        }
                        Spacer(Modifier.width(6.dp))
                        Text(song.language, style = MaterialTheme.typography.labelSmall.copy(fontSize = 10.sp), color = MaterialTheme.colorScheme.onSurfaceVariant)
                    }
                }
            }
        }
    }
}

@Composable
fun SongDetailScreen(song: SongItem) {
    val isUrduTitle = isUrduText(song.title); val isUrduLyrics = isUrduText(song.lyrics)
    val screenWidth = rememberScreenWidthDp()
    val horizontalPadding = when { screenWidth >= 840 -> 120.dp; screenWidth >= 600 -> 60.dp; else -> 24.dp }
    val layoutDir = if (isUrduLyrics) LayoutDirection.Rtl else LayoutDirection.Ltr

    LazyColumn(modifier = Modifier.fillMaxSize(), contentPadding = PaddingValues(horizontal = horizontalPadding, vertical = 24.dp), horizontalAlignment = Alignment.CenterHorizontally) {
        item {
            Column(horizontalAlignment = Alignment.CenterHorizontally) {
                // Category & language badges
                Row(horizontalArrangement = Arrangement.Center, verticalAlignment = Alignment.CenterVertically) {
                    Surface(shape = RoundedCornerShape(20.dp), color = MaterialTheme.colorScheme.primaryContainer) {
                        Text(song.category.uppercase(), modifier = Modifier.padding(horizontal = 14.dp, vertical = 5.dp), style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.onPrimaryContainer, letterSpacing = 2.sp, fontWeight = FontWeight.Bold)
                    }
                    Spacer(Modifier.width(8.dp))
                    Surface(shape = RoundedCornerShape(20.dp), color = MaterialTheme.colorScheme.surfaceVariant) {
                        Text(song.language, modifier = Modifier.padding(horizontal = 12.dp, vertical = 5.dp), style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.onSurfaceVariant, fontWeight = FontWeight.Medium)
                    }
                }
                Spacer(Modifier.height(18.dp))
                if (song.heading != null) {
                    Text(song.heading, style = if (isUrduText(song.heading)) MaterialTheme.typography.titleMedium.copy(fontFamily = LocalUrduFont.current, fontSize = 16.sp) else MaterialTheme.typography.titleMedium, color = MaterialTheme.colorScheme.primary, textAlign = TextAlign.Center)
                    Spacer(Modifier.height(8.dp))
                }
                CompositionLocalProvider(LocalLayoutDirection provides layoutDir) {
                    Text(song.title, style = if (isUrduTitle) MaterialTheme.typography.headlineMedium.copy(fontFamily = LocalUrduFont.current, fontSize = 28.sp, lineHeight = 44.sp, fontWeight = FontWeight.Bold) else MaterialTheme.typography.headlineMedium.copy(fontWeight = FontWeight.Bold), textAlign = TextAlign.Center, color = MaterialTheme.colorScheme.onBackground)
                }
                Spacer(Modifier.height(20.dp))
                // Divider
                Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.Center, modifier = Modifier.fillMaxWidth()) {
                    Box(Modifier.width(40.dp).height(1.dp).background(brush = Brush.horizontalGradient(listOf(Color.Transparent, MaterialTheme.colorScheme.primary.copy(alpha = 0.4f)))))
                    Spacer(Modifier.width(8.dp)); Box(Modifier.size(6.dp).clip(CircleShape).background(MaterialTheme.colorScheme.primary.copy(alpha = 0.6f))); Spacer(Modifier.width(8.dp))
                    Box(Modifier.width(40.dp).height(1.dp).background(brush = Brush.horizontalGradient(listOf(MaterialTheme.colorScheme.primary.copy(alpha = 0.4f), Color.Transparent))))
                }
                Spacer(Modifier.height(28.dp))
                CompositionLocalProvider(LocalLayoutDirection provides layoutDir) {
                    Text(song.lyrics, style = if (isUrduLyrics) MaterialTheme.typography.bodyLarge.copy(fontFamily = LocalUrduFont.current, fontSize = 22.sp, lineHeight = 52.sp) else MaterialTheme.typography.bodyLarge.copy(fontSize = 16.sp, lineHeight = 30.sp), textAlign = TextAlign.Center, color = MaterialTheme.colorScheme.onBackground)
                }
                Spacer(Modifier.height(80.dp))
            }
        }
    }
}
