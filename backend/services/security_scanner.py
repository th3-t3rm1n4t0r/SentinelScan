
import os
import re

patterns = {
    "sql_injection": r"SELECT .* \\+",
    "hardcoded_password": r"password\\s*=",
    "api_key_exposed": r"api_key"
}

def scan_code(folder):

    results = []

    for root, _, files in os.walk(folder):

        for file in files:

            if file.endswith(".py"):

                path = os.path.join(root, file)

                with open(path, "r", errors="ignore") as f:

                    code = f.read()

                    for name, pattern in patterns.items():

                        if re.search(pattern, code):

                            results.append({
                                "file": file,
                                "issue": name,
                                "severity": "High"
                            })

    return results
