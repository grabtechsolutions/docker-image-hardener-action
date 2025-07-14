def parse_dockerfile(path):
    issues = []
    with open(path, "r") as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        if "latest" in line and line.strip().startswith("FROM"):
            issues.append(f"Line {i+1}: Avoid using 'latest' tag — use a specific version.")
        if line.strip().startswith("ADD "):
            issues.append(f"Line {i+1}: Prefer 'COPY' over 'ADD' unless needed.")
    if not any("USER" in line for line in lines):
        issues.append("Missing 'USER' instruction — avoid running as root.")

    return issues
