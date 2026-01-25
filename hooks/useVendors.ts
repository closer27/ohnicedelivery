"use client";

import { useState, useEffect } from "react";
import { VendorConfig, VendorConfigMap } from "@/types";
import { DEFAULT_VENDORS } from "@/lib/vendors";

const STORAGE_KEY = "ohnice_vendors_v8";

export function useVendors() {
    const [vendors, setVendors] = useState<VendorConfigMap>({});

    // Load from storage or default on mount
    useEffect(() => {
        const stored = localStorage.getItem(STORAGE_KEY);
        if (stored) {
            try {
                setVendors(JSON.parse(stored));
            } catch (e) {
                console.error("Failed to parse vendor config", e);
                loadDefaults();
            }
        } else {
            loadDefaults();
        }
    }, []);

    const loadDefaults = () => {
        const map: VendorConfigMap = {};
        DEFAULT_VENDORS.forEach((v) => {
            map[v.id] = v;
        });
        setVendors(map);
        save(map);
    };

    const save = (newVendors: VendorConfigMap) => {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(newVendors));
    };

    const updateVendor = (id: string, config: VendorConfig) => {
        const newVendors = { ...vendors, [id]: config };
        setVendors(newVendors);
        save(newVendors);
    };

    const resetVendors = () => {
        loadDefaults();
    };

    return { vendors, updateVendor, resetVendors };
}
