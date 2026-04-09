import { useLocation, useNavigate } from "react-router-dom";
import { motion } from "framer-motion";

export default function Results() {
  const location = useLocation();
  const navigate = useNavigate();

  let data = location.state?.data;

  if (!data) {
    data = {
      filename: "user_data.py",
      issues: [
        { name: "SQL Injection", severity: "High" },
        { name: "Hardcoded API Key", severity: "Critical" },
        { name: "Insecure Library", severity: "Medium" },
      ],
      files: ["user_data.py", "app.js", "config.js"],
    };
  }

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="min-h-screen bg-gradient-to-br from-black via-gray-900 to-black text-white p-8"
    >
      <h1 className="text-3xl font-bold mb-8">
        📊 Scan Results: {data.filename}
      </h1>

      {/* ISSUES */}
      <div className="space-y-4 mb-10">
        {data.issues.map((issue, i) => (
          <motion.div
            key={i}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.2 }}
            whileHover={{ scale: 1.03 }}
            className="bg-white/5 border border-white/10 p-5 rounded-xl flex justify-between items-center"
          >
            <span className="text-lg">{issue.name}</span>

            <span
              className={`px-3 py-1 rounded-full text-sm ${
                issue.severity === "Critical"
                  ? "bg-red-500/20 text-red-400"
                  : issue.severity === "High"
                  ? "bg-orange-500/20 text-orange-400"
                  : "bg-yellow-500/20 text-yellow-400"
              }`}
            >
              {issue.severity}
            </span>
          </motion.div>
        ))}
      </div>

      {/* FILES */}
      <h2 className="text-xl mb-4">📁 Files Scanned</h2>

      <div className="space-y-3 mb-10">
        {data.files.map((file, i) => (
          <motion.div
            key={i}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.4 + i * 0.1 }}
            className="bg-white/5 border border-white/10 p-4 rounded-xl flex justify-between items-center"
          >
            <span>{file}</span>
            <span className="text-green-400">●●●</span>
          </motion.div>
        ))}
      </div>

      {/* BUTTON */}
      <motion.button
        whileHover={{ scale: 1.1 }}
        whileTap={{ scale: 0.9 }}
        onClick={() => navigate("/fix")}
        className="bg-green-500 hover:bg-green-600 px-6 py-3 rounded-xl font-semibold"
      >
        Generate Fix →
      </motion.button>
    </motion.div>
  );
}