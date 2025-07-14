from pathlib import Path

def rewrite_dockerfile(input_path, output_path="Dockerfile.hardened"):
    input_path = Path(input_path)
    lines = input_path.read_text().splitlines()
    rewritten = []

    user_found = False

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("FROM") and "latest" in line:
            line = line.replace("latest", "3.11.9-slim")
        if stripped.startswith("ADD "):
            line = line.replace("ADD", "COPY")
        if stripped.startswith("USER"):
            user_found = True
        rewritten.append(line)

    if not user_found:
        rewritten.append("\nUSER nonroot")

    output = Path(output_path)
    output.write_text("\n".join(rewritten))
    print(f"✅ Hardened Dockerfile written to: {output}")
