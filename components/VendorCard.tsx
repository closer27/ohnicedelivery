"use client";

import React, { useState } from "react";
import { VendorConfig } from "@/types";
import { Button } from "@/components/ui/button";
import { Check, Edit, Save } from "lucide-react";

interface VendorMappingRowProps {
    label: string;
    field: keyof VendorConfig["mappings"];
    value: number;
    onChange: (val: number) => void;
    isEditing: boolean;
}

function VendorMappingRow({
    label,
    value,
    onChange,
    isEditing,
}: VendorMappingRowProps) {
    return (
        <div className="flex items-center justify-between py-2 border-b last:border-0 border-slate-100">
            <span className="text-sm text-slate-600">{label}</span>
            {isEditing ? (
                <input
                    type="number"
                    value={value}
                    onChange={(e) => onChange(parseInt(e.target.value) || 0)}
                    className="w-16 px-2 py-1 text-sm border rounded text-right"
                />
            ) : (
                <code className="text-sm font-mono bg-slate-100 px-2 py-0.5 rounded text-slate-700">
                    Col {value}
                </code>
            )}
        </div>
    );
}

interface VendorCardProps {
    vendor: VendorConfig;
    onUpdate: (config: VendorConfig) => void;
}

export function VendorCard({ vendor, onUpdate }: VendorCardProps) {
    const [isEditing, setIsEditing] = useState(false);
    const [config, setConfig] = useState(vendor);

    const handleSave = () => {
        onUpdate(config);
        setIsEditing(false);
    };

    const handleChange = (field: keyof VendorConfig["mappings"], val: number) => {
        setConfig((prev) => ({
            ...prev,
            mappings: { ...prev.mappings, [field]: val },
        }));
    };

    return (
        <div className="bg-white rounded-lg border shadow-sm p-4 w-full">
            <div className="flex items-center justify-between mb-4">
                <div>
                    <h3 className="font-bold text-slate-900">{vendor.name}</h3>
                    <p className="text-xs text-slate-500 flex flex-wrap gap-1 mt-1">
                        {vendor.identifiers.map((id) => (
                            <span
                                key={id}
                                className="bg-primary/10 text-primary px-1.5 py-0.5 rounded"
                            >
                                {id}
                            </span>
                        ))}
                    </p>
                </div>
                <Button
                    size="sm"
                    variant={isEditing ? "default" : "outline"}
                    onClick={isEditing ? handleSave : () => setIsEditing(true)}
                >
                    {isEditing ? <Check className="h-4 w-4 mr-1" /> : <Edit className="h-4 w-4 mr-1" />}
                    {isEditing ? "Save" : "Edit"}
                </Button>
            </div>

            <div className="space-y-1">
                <div className="flex items-center justify-between py-2 border-b border-primary/20 bg-primary/5 -mx-4 px-4 mb-2">
                    <span className="text-sm font-semibold text-primary">Start Row (0-based)</span>
                    {isEditing ? (
                        <input
                            type="number"
                            value={config.startRow !== undefined ? config.startRow : 1}
                            onChange={(e) => setConfig(prev => ({ ...prev, startRow: parseInt(e.target.value) || 0 }))}
                            className="w-16 px-2 py-1 text-sm border rounded text-right"
                        />
                    ) : (
                        <code className="text-sm font-mono font-bold text-primary">
                            Row {config.startRow !== undefined ? config.startRow : 1}
                        </code>
                    )}
                </div>
                <VendorMappingRow
                    label="Order Number"
                    field="order_num"
                    value={config.mappings.order_num}
                    onChange={(v) => handleChange("order_num", v)}
                    isEditing={isEditing}
                />
                <VendorMappingRow
                    label="Product Name"
                    field="product_name"
                    value={config.mappings.product_name}
                    onChange={(v) => handleChange("product_name", v)}
                    isEditing={isEditing}
                />
                <VendorMappingRow
                    label="Option"
                    field="product_option"
                    value={config.mappings.product_option}
                    onChange={(v) => handleChange("product_option", v)}
                    isEditing={isEditing}
                />
                <VendorMappingRow
                    label="Recipient Name"
                    field="recipient_name"
                    value={config.mappings.recipient_name}
                    onChange={(v) => handleChange("recipient_name", v)}
                    isEditing={isEditing}
                />
                <VendorMappingRow
                    label="Phone"
                    field="recipient_phone"
                    value={config.mappings.recipient_phone}
                    onChange={(v) => handleChange("recipient_phone", v)}
                    isEditing={isEditing}
                />
                <VendorMappingRow
                    label="Quantity"
                    field="product_quantity"
                    value={config.mappings.product_quantity}
                    onChange={(v) => handleChange("product_quantity", v)}
                    isEditing={isEditing}
                />
                <VendorMappingRow
                    label="Address"
                    field="address"
                    value={config.mappings.address}
                    onChange={(v) => handleChange("address", v)}
                    isEditing={isEditing}
                />
            </div>
        </div>
    );
}
