"use client";

import { useState } from "react";
import { FileUploader } from "@/components/FileUploader";
import { useVendors } from "@/hooks/useVendors";
import { readExcelFile, detectVendor, mapRowToOrder, generateUnifiedExcel } from "@/lib/excel";
import { OrderData } from "@/types";
import { Button } from "@/components/ui/button";
import { VendorCard } from "@/components/VendorCard";
import { Download, Loader2, Settings2, CheckCircle2, AlertCircle } from "lucide-react";
import { cn } from "@/lib/utils";

export default function Home() {
  const { vendors, updateVendor, resetVendors } = useVendors();
  const [files, setFiles] = useState<File[]>([]);
  const [isProcessing, setIsProcessing] = useState(false);
  const [processedOrders, setProcessedOrders] = useState<OrderData[]>([]);
  const [logs, setLogs] = useState<string[]>([]);
  const [showConfig, setShowConfig] = useState(false);

  // Helper log
  const addLog = (msg: string) => setLogs((prev) => [...prev, msg]);

  const handleProcess = async () => {
    setIsProcessing(true);
    setLogs([]);
    setProcessedOrders([]);

    const allOrders: OrderData[] = [];

    try {
      for (const file of files) {
        addLog(`Reading file: ${file.name}...`);

        // 1. Read
        const rows = await readExcelFile(file);
        if (rows.length < 1) {
          addLog(`Warning: ${file.name} is empty.`);
          continue;
        }

        // 2. Identify Vendor
        const vendorId = detectVendor(file.name, vendors);
        if (!vendorId) {
          addLog(`Error: Could not identify vendor for ${file.name}. check filename.`);
          continue;
        }
        const vendor = vendors[vendorId];
        addLog(`Identified as: ${vendor.name}`);

        // 3. Map
        // Assume row 0 is header? Or vendors start at different rows?
        // Python code didn't specify start row explicitly, seemingly simply iterated.
        // We will assume standard headers at row 0 (index 0) and data starts at 1,
        // UNLESS row count is small.
        // Actually, Python `seller.py` indices are 0-based.
        // Safest bets: Skip 1st row (header).

        let fileOrdersCount = 0;
        // Start from configured startRow or default to 1 (skipping header)
        const startRowIndex = vendor.startRow !== undefined ? vendor.startRow : 1;

        for (let i = startRowIndex; i < rows.length; i++) {
          const row = rows[i];
          if (!row || row.length === 0) continue;

          try {
            const order = mapRowToOrder(row, vendor, i);
            // Basic validation: if no recipient name, skip
            if (!order.recipient_name && !order.order_num) continue;

            allOrders.push(order);
            fileOrdersCount++;
          } catch (e) {
            console.error(e);
          }
        }
        addLog(`Processed ${fileOrdersCount} orders from ${file.name}`);
      }

      setProcessedOrders(allOrders);
      addLog(`Done! Total ${allOrders.length} orders ready to merge.`);

    } catch (error) {
      console.error(error);
      addLog(`Critical Error: ${String(error)}`);
    } finally {
      setIsProcessing(false);
    }
  };

  const handleDownload = async () => {
    const data = await generateUnifiedExcel(processedOrders);
    const blob = new Blob([data as unknown as BlobPart], { type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" });
    const url = URL.createObjectURL(blob);

    const now = new Date();
    const dateStr = `${now.getFullYear().toString().slice(2)}${(now.getMonth() + 1).toString().padStart(2, '0')}${now.getDate().toString().padStart(2, '0')}`;
    const filename = `배송지_오나이스피스_${dateStr}.xlsx`;

    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
  };

  return (
    <main className="min-h-screen p-8 max-w-5xl mx-auto space-y-12">
      {/* Header */}
      {/* Header / Hero Section */}
      <div className="flex flex-col items-center justify-center text-center gap-8 py-10">
        <div className="w-64 md:w-80">
          {/* Using Next.js Image would be better but standard img is fine for now if configured */}
          <img src="/bg_pattern.png" alt="Oh Nice Piece" className="w-full h-auto" />
        </div>

        <h1 className="text-4xl md:text-6xl font-extrabold tracking-tight text-slate-900 uppercase leading-tight">
          Have a great day<br />
          with<br />
          onp delivery
        </h1>

        <div className="absolute top-6 left-6 md:top-10 md:left-10">
          <span className="font-bold text-xl tracking-tighter text-slate-900">oh nice piece</span>
        </div>

        <Button
          variant="outline"
          onClick={() => setShowConfig(!showConfig)}
          className={cn("absolute top-6 right-6 md:top-10 md:right-10", showConfig && "bg-slate-100")}
        >
          <Settings2 className="mr-2 h-4 w-4" />
          {showConfig ? "Hide Settings" : "Vendor Settings"}
        </Button>
      </div>

      {/* Vendor Config Section */}
      {showConfig && (
        <section className="space-y-6 bg-slate-50 p-6 rounded-2xl border animate-in slide-in-from-top-4">
          <div className="flex items-center justify-between">
            <h2 className="text-xl font-bold text-slate-800">Vendor Configuration</h2>
            <Button variant="ghost" size="sm" onClick={() => {
              if (confirm("Reset all vendor settings to default?")) {
                resetVendors();
              }
            }}>
              Reset to Defaults
            </Button>
          </div>
          <p className="text-slate-500 text-sm mb-4">
            Adjust column indices if vendor file formats change. Changes are saved automatically in your browser.
          </p>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {Object.values(vendors).map((v) => (
              <VendorCard key={v.id} vendor={v} onUpdate={(c) => updateVendor(v.id, c)} />
            ))}
          </div>
        </section>
      )}

      {/* Main Workflow */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-12">
        {/* Left: Upload */}
        <div className="space-y-6">
          <div className="flex items-center gap-2">
            <div className="bg-blue-100 text-blue-700 font-bold h-8 w-8 rounded-full flex items-center justify-center">1</div>
            <h2 className="text-xl font-semibold">Upload Files</h2>
          </div>

          <FileUploader onFilesSelected={setFiles} isLoading={isProcessing} />

          <div className="pt-4">
            <Button
              size="lg"
              className="w-full text-base"
              disabled={files.length === 0 || isProcessing}
              onClick={handleProcess}
            >
              {isProcessing ? (
                <>
                  <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                  Processing...
                </>
              ) : (
                "Process Files"
              )}
            </Button>
          </div>
        </div>

        {/* Right: Status & Download */}
        <div className="space-y-6">
          <div className="flex items-center gap-2">
            <div className="bg-blue-100 text-blue-700 font-bold h-8 w-8 rounded-full flex items-center justify-center">2</div>
            <h2 className="text-xl font-semibold">Result</h2>
          </div>

          <div className="bg-white border rounded-xl p-6 min-h-[300px] shadow-sm flex flex-col">
            {logs.length === 0 && processedOrders.length === 0 ? (
              <div className="flex-1 flex flex-col items-center justify-center text-slate-400">
                <p>Waiting for files...</p>
              </div>
            ) : (
              <div className="flex-1 overflow-y-auto max-h-[300px] font-mono text-sm space-y-1 mb-4">
                {logs.map((log, i) => (
                  <div key={i} className={cn("flex gap-2", log.startsWith("Error") ? "text-red-500" : "text-slate-600")}>
                    <span>&gt;</span>
                    <span>{log}</span>
                  </div>
                ))}
              </div>
            )}

            {processedOrders.length > 0 && (
              <div className="pt-4 border-t mt-auto">
                <div className="flex items-center justify-between mb-4">
                  <div className="flex items-center text-green-600 gap-2">
                    <CheckCircle2 className="h-5 w-5" />
                    <span className="font-semibold">{processedOrders.length} orders merged</span>
                  </div>
                </div>
                <Button
                  className="w-full bg-green-600 hover:bg-green-700 text-white"
                  size="lg"
                  onClick={handleDownload}
                >
                  <Download className="mr-2 h-5 w-5" />
                  Download Unified Excel
                </Button>
              </div>
            )}
          </div>
        </div>
      </div>
      <footer className="py-8 text-center text-slate-400 text-sm">
        Copyright © onpstudio 2026
      </footer>
    </main>
  );
}
