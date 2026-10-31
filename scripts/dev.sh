#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

# Prefer the active Ruby manager; fall back to Homebrew on macOS when needed.
if ! ruby -e 'exit(Gem::Version.new(RUBY_VERSION) >= Gem::Version.new("3.2") ? 0 : 1)' 2>/dev/null; then
  for ruby_bin in /opt/homebrew/opt/ruby/bin /usr/local/opt/ruby/bin; do
    if [[ -x "$ruby_bin/ruby" ]]; then
      export PATH="$ruby_bin:$PATH"
      break
    fi
  done
fi
if ! ruby -e 'exit(Gem::Version.new(RUBY_VERSION) >= Gem::Version.new("3.2") ? 0 : 1)' 2>/dev/null; then
  printf '%s\n' 'Ruby 3.2 or newer is required. Install Ruby 3.3+ and Bundler, then retry.' >&2
  exit 1
fi
export BUNDLE_PATH="${BUNDLE_PATH:-vendor/bundle}"
if ! bundle check >/dev/null 2>&1; then
  printf '%s\n' 'Install the project dependencies first: bundle install' >&2
  exit 1
fi
exec bundle exec jekyll serve --host 127.0.0.1 --port "${PORT:-4000}" "$@"
