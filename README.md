# 🔐 Docker Image Hardener

Secure your Docker images by scanning and analyzing them using [Trivy](https://github.com/aquasecurity/trivy).  
This GitHub Action helps you harden Dockerfiles, identify vulnerabilities, generate SBOM/SARIF reports, and score your image — directly in CI/CD.

---

## 🚀 Features

- 🔍 Trivy scan for vulnerabilities  
- 📄 JSON vulnerability report  
- 🧾 SBOM generation (CycloneDX format)  
- 🧪 SARIF output for GitHub Security tab  
- 📊 Scorecard grading (A/B/C/D)  
- 📝 GitHub Actions summary report  
- 📦 Upload scan artifacts  
- 💡 Supports multiple Dockerfiles/images  

---

## 🧰 Usage

```yaml
jobs:
  harden:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: 🔒 Run Docker Image Hardener
        uses: grabtechsolutions/docker-image-hardener-action/@v1.0.0
        with:
          dockerfile: examples/sample.Dockerfile
          scan: true
          summary: true
          save-json: true
          severity: HIGH,CRITICAL
          sbom: true
          sarif: true
          scorecard: true
```

---

## ⚙️ Inputs

| Name               | Type     | Description                                                               | Required | Default                        |
|--------------------|----------|---------------------------------------------------------------------------|----------|--------------------------------|
| `dockerfile`        | string   | Comma-separated list of Dockerfile paths to scan                          | false    | `""`                           |
| `image`             | string   | Comma-separated list of image names (if already built)                    | false    | `""`                           |
| `scan`              | boolean  | Run Trivy scan on the image                                               | false    | `false`                        |
| `rewrite`           | boolean  | Rewrite the Dockerfile with best practices (coming soon)                  | false    | `false`                        |
| `fail-on-critical`  | boolean  | Fail job if CRITICAL vulnerabilities are found                            | false    | `false`                        |
| `severity`          | string   | Comma-separated severities (e.g., `HIGH,CRITICAL`)                        | false    | `UNKNOWN,LOW,MEDIUM,HIGH,CRITICAL` |
| `summary`           | boolean  | Generate GitHub Summary Table                                             | false    | `false`                        |
| `save-json`         | boolean  | Save scan result as JSON                                                  | false    | `false`                        |
| `sbom`              | boolean  | Generate SBOM in CycloneDX format                                         | false    | `false`                        |
| `sarif`             | boolean  | Generate SARIF report (for GitHub Security tab)                           | false    | `false`                        |
| `scorecard`         | boolean  | Grade image security (A/B/C/D)                                            | false    | `false`                        |
| `output-dir`        | string   | Directory to store scan outputs                                           | false    | `artifact_scan/`              |

---

## 📂 Artifacts

When enabled, the following files are uploaded automatically:

- `*.json` – Trivy scan results  
- `*.sbom.json` – Software Bill of Materials  
- `*.sarif.json` – SARIF security report  

---

## 📘 GitHub Summary Output

A GitHub Actions summary is generated when `summary: true` is passed.

```
## 🛡️ Trivy Scan Summary

| Image                           | Vulnerabilities | Status     | 
|---------------------------------|-----------------|------------|
| harden-test-image-sample:latest | 12              | ❌ Failed  |
```

---

## 📌 Notes

- ⚠️ **Wiz integration will be added soon.**  
- 🛠️ Want custom behavior, additional scanners, or enterprise support?  
  **Contact me directly** — I'm open to custom work and collaboration.

---

## 🧩 Roadmap

- ✅ Multi-image scan support  
- ✅ Scorecard grading  
- ✅ SBOM and SARIF support  
- 🔜 Dockerfile rewriting with best practices  
- 🔜 Wiz CLI scan integration  
- 🔜 PR comment bot support  
- 🔜 GitHub Security tab annotation upload  

---

## 🙋 Support

This action is actively maintained.  
Have an idea, question, or improvement?  
[Open an issue](https://github.com/developer9508/docker-image-hardener-action/issues) or **contact me directly**.

---

## 🧾 License

[MIT](LICENSE)

---

## 🤝 Sponsor or Collaborate

Using this action in production?  
Need enterprise-grade security tooling or custom GitHub Actions?
Want custom DevSecOps tools built for your team?

> I'm open to collaborations on open-source, DevSecOps, or CI/CD tooling.  
> For consulting or enterprise integrations, feel free to connect on [LinkedIn](https://www.linkedin.com/in/bharat-maheshwari-824bb5147) or open an issue.
