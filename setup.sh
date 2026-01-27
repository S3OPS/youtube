#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

print_banner() {
  cat <<'EOF'
╔══════════════════════════════════════════════════════════════╗
║  🧙 One Command to Rule Them All (Setup Script)             ║
║  The Fellowship of the Python 3.12 Install                 ║
╚══════════════════════════════════════════════════════════════╝
EOF
}

command_exists() {
  command -v "$1" >/dev/null 2>&1
}

cleanup_unneeded() {
  echo "🧹 Sweeping the Shire (removing cache clutter)..."
  find "$ROOT_DIR" -type d -name "__pycache__" -prune -exec rm -rf {} + 2>/dev/null || true
  find "$ROOT_DIR" -type f -name "*.pyc" -delete 2>/dev/null || true
  find "$ROOT_DIR" -type f -name ".DS_Store" -delete 2>/dev/null || true
}

install_python_312() {
  if command_exists python3.12; then
    echo "✅ Python 3.12 already in the Fellowship."
    return
  fi

  echo "🗡️  Summoning Python 3.12..."
  if command_exists uv; then
    uv python install 3.12
    return
  fi
  if command_exists apt-get; then
    sudo apt-get update
    sudo apt-get install -y python3.12 python3.12-venv python3.12-distutils
    return
  fi
  if command_exists dnf; then
    sudo dnf install -y python3.12 python3.12-devel
    return
  fi
  if command_exists brew; then
    brew install python@3.12
    return
  fi
  if command_exists winget; then
    winget install -e --id Python.Python.3.12
    return
  fi

  echo "❌ Could not auto-install Python 3.12. Please install it manually:"
  echo "   https://www.python.org/downloads/"
  exit 1
}

install_ffmpeg() {
  if command_exists ffmpeg; then
    echo "✅ ffmpeg already armed."
    return
  fi

  echo "🎥 Forging ffmpeg..."
  if command_exists apt-get; then
    sudo apt-get install -y ffmpeg
    return
  fi
  if command_exists dnf; then
    sudo dnf install -y ffmpeg
    return
  fi
  if command_exists brew; then
    brew install ffmpeg
    return
  fi
  if command_exists winget; then
    winget install -e --id Gyan.FFmpeg
    return
  fi

  echo "⚠️  ffmpeg not found. Install it manually from https://ffmpeg.org/download.html"
}

setup_virtualenv() {
  echo "🧝 Creating the Elven virtual environment..."
  local python_exec="python3.12"
  if ! command_exists "$python_exec"; then
    python_exec="python3"
  fi
  if ! "$python_exec" -c "import sys; sys.exit(0 if sys.version_info[:2] == (3, 12) else 1)"; then
    echo "❌ Python 3.12 is required to continue."
    echo "   Re-run this script after installing Python 3.12."
    exit 1
  fi
  "$python_exec" -m venv "$ROOT_DIR/.venv"

  if [[ -f "$ROOT_DIR/.venv/bin/activate" ]]; then
    # shellcheck disable=SC1091
    source "$ROOT_DIR/.venv/bin/activate"
  elif [[ -f "$ROOT_DIR/.venv/Scripts/activate" ]]; then
    # shellcheck disable=SC1091
    source "$ROOT_DIR/.venv/Scripts/activate"
  else
    echo "❌ Could not activate the virtual environment."
    exit 1
  fi

  python -m pip install --upgrade pip
  python -m pip install -r "$ROOT_DIR/requirements.txt"
}

run_setup_wizard() {
  echo "🪄 Running the setup wizard..."
  python "$ROOT_DIR/setup.py"
}

view_setup_docs() {
  echo "📜 Opening the Red Book of Westmarch (setup docs)..."
  local docs=(SETUP_GUIDE.md README.md QUICKSTART.md CHECKLIST.md TROUBLESHOOTING.md .env.example requirements.txt setup.py)
  local max_bytes=1048576
  local output_bytes=0
  for doc in "${docs[@]}"; do
    if [[ -f "$ROOT_DIR/$doc" ]]; then
      local size
      size=$(wc -c < "$ROOT_DIR/$doc")
      if (( output_bytes + size > max_bytes )); then
        echo
        echo "===== $doc (partial) ====="
        head -n 200 "$ROOT_DIR/$doc"
        echo "…truncated. See $doc for full text."
        output_bytes=$max_bytes
        continue
      fi
      echo
      echo "===== $doc ====="
      cat "$ROOT_DIR/$doc"
      output_bytes=$((output_bytes + size))
    fi
  done
  echo
}

final_message() {
  cat <<'EOF'
✅ Setup complete. The One Command has done its work.

Next steps:
  1. Ensure client_secrets.json is in the project root.
  2. Run the web dashboard: python app.py
  3. Or create a video now: python create_video.py
EOF
}

print_banner
cleanup_unneeded
install_python_312
install_ffmpeg
setup_virtualenv
run_setup_wizard
view_setup_docs
final_message
