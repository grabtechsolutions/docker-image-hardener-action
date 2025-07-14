#!/bin/bash
set -e

SCRIPT_DIR="${GITHUB_ACTION_PATH:-.}"

mkdir -p artifact_scan
echo "::group::🔍 Starting Docker Image Hardener..."

ARGS=()

[[ -n "$INPUT_DOCKERFILE" ]] && DOCKERFILES="$INPUT_DOCKERFILE"
[[ -n "$INPUT_IMAGE" ]] && IMAGES="$INPUT_IMAGE"

[[ "$INPUT_SCAN" == "true" ]] && ARGS+=(--scan)
[[ "$INPUT_REWRITE" == "true" ]] && ARGS+=(--rewrite)
[[ "$INPUT_FAIL_ON_CRITICAL" == "true" ]] && ARGS+=(--fail-on-critical)
[[ "$INPUT_SUMMARY" == "true" ]] && ARGS+=(--summary)
[[ "$INPUT_SAVE_JSON" == "true" ]] && ARGS+=(--save-json)
[[ "$INPUT_SBOM" == "true" ]] && ARGS+=(--sbom)
[[ "$INPUT_SARIF" == "true" ]] && ARGS+=(--sarif)
[[ "$INPUT_SCORECARD" == "true" ]] && ARGS+=(--scorecard)
[[ -n "$INPUT_SEVERITY" ]] && ARGS+=(--severity "$INPUT_SEVERITY")
[[ -n "$INPUT_OUTPUT_DIR" ]] && ARGS+=(--output-dir "$INPUT_OUTPUT_DIR")

# Dockerfile loop
if [[ -n "$DOCKERFILES" ]]; then
  IFS=',' read -ra FILES <<< "$DOCKERFILES"
  for FILE in "${FILES[@]}"; do
    echo "::group::🔎 Analyzing Dockerfile: $FILE"
    python3 "$SCRIPT_DIR/cli/main.py" "$FILE" "${ARGS[@]}"
    echo "::endgroup::"
  done
fi

# Image scan loop
if [[ -n "$IMAGES" ]]; then
  IFS=',' read -ra IMAGE_LIST <<< "$IMAGES"
  for IMG in "${IMAGE_LIST[@]}"; do
    echo "::group::🛡️ Scanning image: $IMG"
    python3 /app/cli/main.py --scan-image "$IMG" "${ARGS[@]}"
    echo "::endgroup::"
  done
fi

echo "::endgroup::"

# PR comment (optional)
if [[ "$INPUT_SUMMARY" == "true" && "$GITHUB_EVENT_NAME" == "pull_request" ]]; then
  echo "::group::📣 Posting PR comment..."
  python3 "$SCRIPT_DIR/cli/post_pr_comment.py"
  echo "::endgroup::"
fi
