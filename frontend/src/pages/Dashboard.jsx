import { useLocation, useNavigate } from "react-router-dom";
import { motion } from "framer-motion";

export default function Dashboard() {
  const location = useLocation();
  const navigate = useNavigate();

  const repo = location.state?.repo;

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="min-h-screen bg-gradient-to-br from-black via-gray-900 to-black text-white p-10"
    >
      {/* HEADER */}
      <motion.div
        initial={{ y: -30, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        className="mb-10"
      >
        <h1 className="text-3xl font-bold">🚀 Scan Dashboard</h1>
        <p className="text-gray-400 mt-2">
          Repo: {repo || "No repo provided"}
        </p>
      </motion.div>

      {/* MAIN GRID */}
      <div className="grid md:grid-cols-2 gap-10">

        {/* 🔥 LEFT CARD (CIRCLE SCORE) */}
        <motion.div
          initial={{ scale: 0.8, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{ duration: 0.5 }}
          whileHover={{ scale: 1.05 }}
          className="bg-white/5 border border-white/10 rounded-2xl p-10 flex flex-col items-center justify-center shadow-xl"
        >
          <h2 className="text-gray-400 mb-6">Security Score</h2>

          <div className="relative flex items-center justify-center">
            <div className="w-44 h-44 rounded-full border-[10px] border-orange-500 flex items-center justify-center text-4xl font-bold">
              82
            </div>
          </div>

          <motion.button
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.9 }}
            onClick={() =>
              navigate("/results", {
                state: {
                  data: {
                    filename: "user_data.py",
                    issues: [
                      { name: "SQL Injection", severity: "High" },
                      { name: "API Key Exposure", severity: "Critical" },
                      { name: "Insecure Library", severity: "Medium" },
                    ],
                    files: ["user_data.py", "app.js", "config.js"],
                  },
                },
              })
            }
            className="mt-8 bg-green-500 hover:bg-green-600 px-6 py-3 rounded-xl font-semibold"
          >
            View Detailed Results →
          </motion.button>
        </motion.div>

        {/* 🔥 RIGHT SIDE STATS */}
        <motion.div
          initial={{ x: 80, opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
          transition={{ delay: 0.3 }}
          className="space-y-6"
        >
          <motion.div
            whileHover={{ scale: 1.05 }}
            className="bg-white/5 border border-white/10 p-6 rounded-xl"
          >
            <h3 className="text-red-400 text-lg">🔴 Critical Issues</h3>
            <p className="text-3xl font-bold mt-2">1</p>
          </motion.div>

          <motion.div
            whileHover={{ scale: 1.05 }}
            className="bg-white/5 border border-white/10 p-6 rounded-xl"
          >
            <h3 className="text-orange-400 text-lg">🟠 High Issues</h3>
            <p className="text-3xl font-bold mt-2">2</p>
          </motion.div>

          <motion.div
            whileHover={{ scale: 1.05 }}
            className="bg-white/5 border border-white/10 p-6 rounded-xl"
          >
            <h3 className="text-yellow-400 text-lg">🟡 Medium Issues</h3>
            <p className="text-3xl font-bold mt-2">3</p>
          </motion.div>
        </motion.div>
      </div>
    </motion.div>
  );
}