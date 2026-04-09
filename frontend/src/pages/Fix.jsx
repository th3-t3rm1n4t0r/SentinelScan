import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";

export default function Fix() {
  const navigate = useNavigate();

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="min-h-screen bg-gradient-to-br from-black via-gray-900 to-black text-white p-8"
    >
      <h1 className="text-3xl font-bold mb-8">🛠 Fix Suggestions</h1>

      <div className="grid md:grid-cols-2 gap-6">
        <motion.div
          initial={{ x: -50, opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
          className="bg-red-500/10 border border-red-500/30 p-5 rounded-xl"
        >
          ❌ Vulnerable Code
        </motion.div>

        <motion.div
          initial={{ x: 50, opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
          className="bg-green-500/10 border border-green-500/30 p-5 rounded-xl"
        >
          ✅ Fixed Code
        </motion.div>
      </div>

      <motion.button
        whileHover={{ scale: 1.1 }}
        whileTap={{ scale: 0.9 }}
        onClick={() => navigate("/report")}
        className="bg-blue-500 px-6 py-3 rounded-xl mt-6"
      >
        Generate Report →
      </motion.button>
    </motion.div>
  );
}