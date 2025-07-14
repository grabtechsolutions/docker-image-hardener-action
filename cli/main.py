import argparse
import os
import sys
from pathlib import Path
from dockerfile_parser import parse_dockerfile
from trivy_scanner import run_trivy_scan, run_image_scan
from dockerfile_rewriter import rewrite_dockerfile

def resolve_output_dir(user_output_dir=None):
    base_dir = user_output_dir or os.environ.get("GITHUB_WORKSPACE") or os.getcwd()
    return os.path.join(base_dir, "artifact_scan")

def main():
    parser = argparse.ArgumentParser(description="Docker Image Hardening Toolkit")
    parser.add_argument("dockerfile", nargs="?", help="Path to the Dockerfile")
    parser.add_argument("--scan-image", help="Scan pre-built image directly")
    parser.add_argument("--scan", action="store_true", help="Run Trivy scan")
    parser.add_argument("--rewrite", action="store_true", help="Rewrite Dockerfile with best practices")
    parser.add_argument("--fail-on-critical", action="store_true", help="Fail if CRITICAL vulnerabilities are found")
    parser.add_argument("--severity", default="UNKNOWN,LOW,MEDIUM,HIGH,CRITICAL", help="Trivy severity filter")
    parser.add_argument("--summary", action="store_true", help="Generate GitHub Actions summary")
    parser.add_argument("--save-json", action="store_true", help="Save Trivy results to JSON file")
    parser.add_argument("--sbom", action="store_true", help="Generate SBOM (Software Bill of Materials)")
    parser.add_argument("--sarif", action="store_true", help="Generate SARIF report")
    parser.add_argument("--scorecard", action="store_true", help="Generate security scorecard")
    parser.add_argument("--output-dir", help="Base directory for outputs (default: auto-detect)")

    args = parser.parse_args()
    output_dir = resolve_output_dir(args.output_dir)

    if args.scan_image:
        run_image_scan(
            image_name=args.scan_image,
            severity=args.severity,
            save_json=args.save_json,
            summary=args.summary,
            fail_on_critical=args.fail_on_critical,
            sbom=args.sbom,
            sarif=args.sarif,
            scorecard=args.scorecard,
            output_dir=output_dir
        )
        return

    if not args.dockerfile:
        print("❌ Dockerfile path is required unless --scan-image is used.")
        sys.exit(1)

    print(f"🔍 Analyzing {args.dockerfile}...")
    issues = parse_dockerfile(args.dockerfile)

    if not args.rewrite:
        for issue in issues:
            print(f"::warning::{issue}")
    else:
        rewrite_dockerfile(args.dockerfile)

    if args.scan:
        run_trivy_scan(
            dockerfile_path=args.dockerfile,
            severity=args.severity,
            save_json=args.save_json,
            summary=args.summary,
            fail_on_critical=args.fail_on_critical,
            sbom=args.sbom,
            sarif=args.sarif,
            scorecard=args.scorecard,
            output_dir=output_dir
        )

if __name__ == "__main__":
    main()
