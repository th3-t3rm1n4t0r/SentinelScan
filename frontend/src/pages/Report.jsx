import html2canvas from "html2canvas";
import jsPDF from "jspdf";

function Report() {

  const downloadPDF = async () => {
    const element = document.getElementById("report-content");

    const canvas = await html2canvas(element, {
      scale: 2,
      useCORS: true,
      backgroundColor: "#0a0a0a"
    });

    const imgData = canvas.toDataURL("image/png");

    const pdf = new jsPDF("p", "mm", "a4");

    const pageWidth = 210;
    const pageHeight = 297;

    const imgWidth = pageWidth;
    const imgHeight = (canvas.height * imgWidth) / canvas.width;

    // 🔥 PERFECT CENTER ALIGN
    const y = (pageHeight - imgHeight) / 2;

    pdf.addImage(imgData, "PNG", 0, y, imgWidth, imgHeight);

    pdf.save("report.pdf");
  };

  return (
    <div className="min-h-screen bg-[#0a0a0a] text-white p-8 flex justify-center items-start">

      <div id="report-content" className="w-full max-w-3xl bg-[#0a0a0a] p-6 rounded-xl">

        <h1 className="text-3xl font-bold mb-8">📄 Security Audit Report</h1>

        {/* SCORE */}
        <div className="bg-white/5 border border-white/10 rounded-xl p-6 mb-8">
          <p className="text-gray-400">Health Score</p>
          <h2 className="text-5xl text-orange-400 font-bold">82</h2>
        </div>

        {/* STATS */}
        <div className="space-y-4 mb-8">
          <div className="border border-red-500/30 p-4 rounded-xl flex justify-between">
            <span>Critical Issues</span>
            <span className="text-red-400">5</span>
          </div>

          <div className="border border-orange-500/30 p-4 rounded-xl flex justify-between">
            <span>High Risks</span>
            <span className="text-orange-400">12</span>
          </div>

          <div className="border border-yellow-500/30 p-4 rounded-xl flex justify-between">
            <span>Medium Risks</span>
            <span className="text-yellow-400">8</span>
          </div>
        </div>

        {/* PROGRESS */}
        <div className="h-2 bg-gray-800 rounded-full mb-8 overflow-hidden">
          <div className="h-full bg-gradient-to-r from-red-500 via-orange-400 to-yellow-400 w-[70%]"></div>
        </div>

        {/* BUTTON */}
        <button
          onClick={downloadPDF}
          className="bg-green-500 hover:bg-green-600 px-6 py-3 rounded-xl"
        >
          Download PDF
        </button>

      </div>
    </div>
  );
}

export default Report;