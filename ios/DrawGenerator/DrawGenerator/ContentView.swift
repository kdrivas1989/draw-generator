import SwiftUI
import WebKit

struct ContentView: View {
    var body: some View {
        WebView()
            .edgesIgnoringSafeArea(.all)
    }
}

struct WebView: UIViewRepresentable {
    func makeUIView(context: Context) -> WKWebView {
        let configuration = WKWebViewConfiguration()
        configuration.allowsInlineMediaPlayback = true

        let webView = WKWebView(frame: .zero, configuration: configuration)
        webView.isOpaque = false
        webView.backgroundColor = UIColor(red: 17/255, green: 24/255, blue: 39/255, alpha: 1)
        webView.scrollView.backgroundColor = UIColor(red: 17/255, green: 24/255, blue: 39/255, alpha: 1)

        // Load the local HTML file
        if let htmlPath = Bundle.main.path(forResource: "index", ofType: "html", inDirectory: "web") {
            let htmlUrl = URL(fileURLWithPath: htmlPath)
            let webDirectory = htmlUrl.deletingLastPathComponent()
            webView.loadFileURL(htmlUrl, allowingReadAccessTo: webDirectory)
        }

        return webView
    }

    func updateUIView(_ uiView: WKWebView, context: Context) {}
}

#Preview {
    ContentView()
}
