import { BrowserRouter, Routes, Route, useLocation, useNavigate } from "react-router-dom";
import { AnimatePresence, motion } from "framer-motion";
import { useState } from "react";

import Dashboard from "./pages/Dashboard";
import Results from "./pages/Results";
import Fix from "./pages/Fix";
import Report from "./pages/Report";

function Home() {
  const navigate = useNavigate();
  const [repo, setRepo] = useState("");
  const [loading, setLoading] = useState(false);

  const handleScan = () => {
    if (!repo) return alert("Enter GitHub repo link");

    setLoading(true);

    setTimeout(() => {
      navigate("/dashboard", { state: { repo } });
    }, 1500);
  };

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="bg-black text-white h-screen flex flex-col items-center justify-center"
    >
      <motion.h1
        initial={{ scale: 0.8 }}
        animate={{ scale: 1 }}
        className="text-5xl font-bold"
      >
        SentinelScan 🔥
      </motion.h1>

      <motion.input
        initial={{ y: 30, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ delay: 0.3 }}
        type="text"
        placeholder="Paste GitHub repo link..."
        value={repo}
        onChange={(e) => setRepo(e.target.value)}
        className="mt-6 px-4 py-2 rounded-lg text-black w-80"
      />

      <motion.button
        whileHover={{ scale: 1.1 }}
        whileTap={{ scale: 0.9 }}
        onClick={handleScan}
        className="bg-orange-500 mt-4 px-6 py-3 rounded-xl"
      >
        {loading ? "Scanning..." : "Scan Repo"}
      </motion.button>
    </motion.div>
  );
}

function AnimatedRoutes() {
  const location = useLocation();

  return (
    <AnimatePresence mode="wait">
      <Routes location={location} key={location.pathname}>
        <Route path="/" element={<Home />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/results" element={<Results />} />
        <Route path="/fix" element={<Fix />} />
        <Route path="/report" element={<Report />} />
      </Routes>
    </AnimatePresence>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <AnimatedRoutes />
    </BrowserRouter>
  );
}