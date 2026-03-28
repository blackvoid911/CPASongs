<?php
/**
 * Bible API for CPA App
 * Place this file at: http://localhost/cpa/pages/bible.php
 *
 * Usage: bible.php?book=Genesis&chapter=1
 * Returns: JSON array of verses
 */

header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');

// Database connection (adjust these settings)
$host = 'localhost';
$dbname = 'cpa_bible';
$username = 'root';
$password = '';

try {
    $pdo = new PDO("mysql:host=$host;dbname=$dbname;charset=utf8mb4", $username, $password);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
} catch (PDOException $e) {
    echo json_encode(['error' => 'Database connection failed']);
    exit;
}

// Get parameters
$book = isset($_GET['book']) ? $_GET['book'] : '';
$chapter = isset($_GET['chapter']) ? (int)$_GET['chapter'] : 1;

if (empty($book)) {
    echo json_encode(['error' => 'Book parameter required']);
    exit;
}

// Query verses
// Adjust table/column names to match your database structure
$sql = "SELECT verse_number as verse, verse_text as text
        FROM bible_verses
        WHERE book_name = :book AND chapter_number = :chapter
        ORDER BY verse_number";

try {
    $stmt = $pdo->prepare($sql);
    $stmt->execute([
        ':book' => $book,
        ':chapter' => $chapter
    ]);

    $verses = $stmt->fetchAll(PDO::FETCH_ASSOC);

    // Convert verse numbers to integers
    foreach ($verses as &$verse) {
        $verse['verse'] = (int)$verse['verse'];
    }

    echo json_encode($verses);

} catch (PDOException $e) {
    echo json_encode(['error' => 'Query failed: ' . $e->getMessage()]);
}
?>

