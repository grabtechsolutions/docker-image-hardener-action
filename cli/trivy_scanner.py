import subprocess
import os
from pathlib import Path
from summary import append_to_summary
import json

def run_trivy_scan(
    dockerfile_path,
    severity="HIGH,CRITICAL",
    save_json=False,
    summary=False,
    fail_on_critical=False,
    sbom=False,
    sarif=False,
    scorecard=False,
    output_dir="artifact_scan"
):
    dockerfile_path = Path(dockerfile_path).resolve()
    image_tag = f"harden-test-image-{dockerfile_path.stem}:latest"
    dockerfile_dir = dockerfile_path.parent
    dockerfile_name = dockerfile_path.name

    # Check if image exists
    inspect_cmd = ["docker", "image", "inspect", image_tag]
    result = subprocess.run(inspect_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if result.returncode != 0:
        print(f"🔧 Building Docker image: {image_tag}")
        build_cmd = ["docker", "build", "-t", image_tag, "-f", dockerfile_name, "."]
        subprocess.run(build_cmd, check=True, cwd=str(dockerfile_dir))
    else:
        print(f"✅ Image already exists: {image_tag}")

    run_image_scan(
        image_name=image_tag,
        severity=severity,
        save_json=save_json,
        summary=summary,
        fail_on_critical=fail_on_critical,
        sbom=sbom,
        sarif=sarif,
        scorecard=scorecard,
        output_dir=output_dir
    )


def run_image_scan(
    image_name,
    severity="HIGH,CRITICAL",
    save_json=False,
    summary=False,
    fail_on_critical=False,
    sbom=False,
    sarif=False,
    scorecard=False,
    output_dir="."
):
    print(f"🛡️ Scanning image: {image_name}")
    output_path = Path(output_dir).resolve()
    os.makedirs(output_path, exist_ok=True)

    json_filename = f"{image_name.replace(':', '_')}_trivy_scan_result.json"
    json_path = output_path / json_filename

    cmd = ["trivy", "image", "--no-progress", "--severity", severity, image_name]
    result = subprocess.run(cmd + ["--format", "json"], capture_output=True, text=True)
    output = result.stdout

    if save_json:
        with open(json_path, "w") as f:
            f.write(output)
        print(f"📄 Trivy JSON saved to: {json_path}")

        # Also log to console for CI visibility
        print("🔍 Trivy Results (condensed):")
        try:
          data = json.loads(output)
          for result in data.get("Results", []):
              target = result.get("Target", "")
              vulns = result.get("Vulnerabilities", [])
              if vulns:
                  print(f"📦 {target}: {len(vulns)} vulnerabilities")
                  for v in vulns[:5]:  # Show only top 5 for brevity
                      print(f"  ❗ {v['VulnerabilityID']} - {v['Severity']} - {v['PkgName']}")
        except Exception as e:
          print(f"⚠️ Could not parse or display Trivy JSON: {e}")

    if sbom:
        sbom_filename = f"{image_name.replace(':', '_')}.sbom.json"
        sbom_path = output_path / sbom_filename
        print("📦 Generating SBOM...")
        sbom_cmd = [
            "trivy", "image",
            "--format", "cyclonedx",
            "--scanners", "license",
            "--output", str(sbom_path),
            image_name
        ]
        subprocess.run(sbom_cmd, check=True)
        print(f"📄 SBOM saved to: {sbom_path}")

    if sarif:
        sarif_filename = f"{image_name.replace(':', '_')}.sarif.json"
        sarif_path = output_path / sarif_filename
        sarif_cmd = [
            "trivy", "image",
            "--no-progress",
            "--format", "sarif",
            "--output", str(sarif_path),
            image_name
        ]
        print("🧪 Generating SARIF report...")
        subprocess.run(sarif_cmd, check=True)
        print(f"📄 SARIF saved to: {sarif_path}")

    if summary:
        vuln_count = output.count('"VulnerabilityID"')
        status = "FAILED" if fail_on_critical and '"CRITICAL"' in output else "PASSED"
        append_to_summary(image_name, vuln_count, status, str(json_path))

    if fail_on_critical and '"CRITICAL"' in output:
        print("::error::❌ CRITICAL vulnerabilities found!")
        exit(1)
    else:
        print("✅ Scan complete.")

    if scorecard:
        try:
            data = json.loads(output)
            crit = sum(
                1 for r in data.get("Results", [])
                for v in r.get("Vulnerabilities", [])
                if v.get("Severity") == "CRITICAL"
            )
            high = sum(
                1 for r in data.get("Results", [])
                for v in r.get("Vulnerabilities", [])
                if v.get("Severity") == "HIGH"
            )
            if crit > 10:
                grade = "🔴 D"
            elif crit > 5:
                grade = "🟠 C"
            elif high > 10:
                grade = "🟡 B"
            else:
                grade = "🟢 A"
            print(f"🎓 Security Scorecard: {grade} (CRITICAL: {crit}, HIGH: {high})")
        except Exception as e:
            print(f"⚠️ Scorecard generation failed: {e}")
