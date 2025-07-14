import os
import json
from pathlib import Path

def append_to_summary(image_name, vuln_count, status, json_file):
    summary_file = os.environ.get("GITHUB_STEP_SUMMARY")
    if not summary_file:
        print("⚠️ GITHUB_STEP_SUMMARY not available.")
        return

    try:
        with open(json_file) as f:
            data = json.load(f)

        vuln_count = sum(len(result.get("Vulnerabilities", [])) for result in data.get("Results", []))

        has_critical = any(
            v.get("Severity") == "CRITICAL"
            for r in data.get("Results", [])
            for v in r.get("Vulnerabilities", [])
        )
        status = "❌ Failed" if has_critical else "✅ Passed"

    except Exception as e:
        vuln_count = "-"
        status = f"⚠️ Error: {e}"

    row = f"| `{image_name}` | `{vuln_count}` | {status} |\n"

    header = (
        "## 🛡️ Trivy Scan Summary\n\n"
        "| Image | Vulnerabilities | Status |\n"
        "|-------|------------------|--------|\n"
    )

    summary_path = Path(summary_file)
    existing = summary_path.read_text() if summary_path.exists() else ""

    if header not in existing:
        summary_path.write_text(header + row, encoding="utf-8")
    else:
        summary_path.write_text(existing + row, encoding="utf-8")
