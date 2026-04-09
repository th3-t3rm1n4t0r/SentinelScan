export const scanRepo = async (repoUrl) => {
  return {
    score: 78,
    repo: repoUrl,
    issues: [
      { title: "SQL Injection", severity: "High" },
      { title: "Hardcoded API Key", severity: "Critical" },
      { title: "Insecure Dependency", severity: "Medium" }
    ],
    files: ["db.js", "config.js", "package.json"]
  };
};