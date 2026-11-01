#!/bin/bash
# 编译 macOS Vision OCR 工具（同目录 ocr.swift -> ocr-vision）
set -e
cd "$(dirname "$0")"
swiftc -O ocr.swift -o ocr-vision
echo "built: $(pwd)/ocr-vision"
