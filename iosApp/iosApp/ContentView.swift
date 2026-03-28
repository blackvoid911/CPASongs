import SwiftUI
import shared
struct ContentView: View {
    var body: some View {
        ComposeView()
            .ignoresSafeArea(.all) // Compose handles insets via WindowInsets
    }
}
/// UIViewControllerRepresentable that bootstraps the KMP Compose UI
struct ComposeView: UIViewControllerRepresentable {
    func makeUIViewController(context: Context) -> UIViewController {
        // Calls CPAMainApp() from the shared Kotlin module
        return MainViewControllerKt.MainViewController()
    }
    func updateUIViewController(_ uiViewController: UIViewController, context: Context) {}
}
