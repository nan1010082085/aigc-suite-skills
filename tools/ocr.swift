// macOS Vision OCR CLI: ocr-vision <image> [image...] -> text to stdout (pages separated by \f)
import Foundation
import Vision
import AppKit

for path in CommandLine.arguments.dropFirst() {
    let url = URL(fileURLWithPath: path)
    guard let image = NSImage(contentsOf: url),
          let cg = image.cgImage(forProposedRect: nil, context: nil, hints: nil) else {
        FileHandle.standardError.write("cannot load \(path)\n".data(using: .utf8)!)
        continue
    }
    let req = VNRecognizeTextRequest()
    req.recognitionLevel = .accurate
    req.recognitionLanguages = ["zh-Hans", "en-US"]
    req.usesLanguageCorrection = true
    let handler = VNImageRequestHandler(cgImage: cg, options: [:])
    do {
        try handler.perform([req])
    } catch {
        FileHandle.standardError.write("ocr fail \(path): \(error)\n".data(using: .utf8)!)
        continue
    }
    // Group observations into lines by vertical proximity (top to bottom)
    let obs = (req.results ?? []).sorted { a, b in
        if abs(a.boundingBox.midY - b.boundingBox.midY) > 0.008 {
            return a.boundingBox.midY > b.boundingBox.midY
        }
        return a.boundingBox.minX < b.boundingBox.minX
    }
    var lines: [(y: CGFloat, items: [(x: CGFloat, s: String)])] = []
    for o in obs {
        guard let cand = o.topCandidates(1).first else { continue }
        let y = o.boundingBox.midY
        if var last = lines.last, abs(last.y - y) < 0.008 {
            last.items.append((o.boundingBox.minX, cand.string))
            lines[lines.count - 1] = last
        } else {
            lines.append((y, [(o.boundingBox.minX, cand.string)]))
        }
    }
    var out = ""
    for line in lines {
        let sorted = line.items.sorted { $0.x < $1.x }.map { $0.s }
        // Join without spaces; Vision may return per-word segments with ASCII where spaces matter
        out += sorted.joined(separator: "") + "\n"
    }
    print(out, terminator: "\u{0C}\n")
}
