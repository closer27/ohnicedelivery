"use client";

import React, { useCallback, useState } from "react";
import { Upload, X, FileSpreadsheet } from "lucide-react";
import { cn } from "@/lib/utils";

interface FileUploaderProps {
    onFilesSelected: (files: File[]) => void;
    isLoading?: boolean;
}

export function FileUploader({ onFilesSelected, isLoading }: FileUploaderProps) {
    const [isDragging, setIsDragging] = useState(false);
    const [selectedFiles, setSelectedFiles] = useState<File[]>([]);

    const handleDragOver = (e: React.DragEvent) => {
        e.preventDefault();
        setIsDragging(true);
    };

    const handleDragLeave = (e: React.DragEvent) => {
        e.preventDefault();
        setIsDragging(false);
    };

    const handleDrop = (e: React.DragEvent) => {
        e.preventDefault();
        setIsDragging(false);
        if (e.dataTransfer.files?.length) {
            addFiles(Array.from(e.dataTransfer.files));
        }
    };

    const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files?.length) {
            addFiles(Array.from(e.target.files));
        }
    };

    const addFiles = (newFiles: File[]) => {
        const validFiles = newFiles.filter(
            (f) =>
                f.name.endsWith(".xls") ||
                f.name.endsWith(".xlsx") ||
                f.name.endsWith(".csv")
        );
        const updated = [...selectedFiles, ...validFiles];
        setSelectedFiles(updated);
        onFilesSelected(updated);
    };

    const removeFile = (index: number) => {
        const updated = selectedFiles.filter((_, i) => i !== index);
        setSelectedFiles(updated);
        onFilesSelected(updated);
    };

    return (
        <div className="w-full space-y-4">
            <div
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
                onDrop={handleDrop}
                className={cn(
                    "border-2 border-dashed rounded-xl p-10 text-center transition-colors cursor-pointer",
                    isDragging
                        ? "border-primary bg-primary/5"
                        : "border-slate-300 hover:border-primary/50",
                    isLoading && "opacity-50 pointer-events-none"
                )}
                onClick={() => document.getElementById("file-input")?.click()}
            >
                <input
                    id="file-input"
                    type="file"
                    multiple
                    accept=".xls,.xlsx,.csv"
                    className="hidden"
                    onChange={handleFileInput}
                />
                <div className="flex flex-col items-center gap-2">
                    <div className="bg-slate-100 p-4 rounded-full">
                        <Upload className="h-6 w-6 text-slate-600" />
                    </div>
                    <h3 className="text-lg font-semibold text-slate-900">
                        Click or drag files here
                    </h3>
                    <p className="text-sm text-slate-500">
                        Upload Excel (.xls, .xlsx) or CSV files
                    </p>
                </div>
            </div>

            {selectedFiles.length > 0 && (
                <div className="space-y-2">
                    {selectedFiles.map((file, idx) => (
                        <div
                            key={`${file.name}-${idx}`}
                            className="flex items-center justify-between p-3 bg-white border rounded-md shadow-sm"
                        >
                            <div className="flex items-center gap-3">
                                <FileSpreadsheet className="h-5 w-5 text-green-600" />
                                <span className="text-sm font-medium text-slate-700">
                                    {file.name}
                                </span>
                                <span className="text-xs text-slate-400">
                                    {(file.size / 1024).toFixed(1)} KB
                                </span>
                            </div>
                            <button
                                onClick={() => removeFile(idx)}
                                className="text-slate-400 hover:text-red-500"
                            >
                                <X className="h-4 w-4" />
                            </button>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}
