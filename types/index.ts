export interface VendorConfig {
    id: string;
    name: string; // Display name e.g., "TenByTen"

    // Mapping of internal field names to Column Index (0-based)
    mappings: {
        recipient_name: number;
        recipient_phone: number;
        zipcode: number;
        address: number;
        order_num: number;
        product_name: number;
        product_option: number;
        product_quantity: number; // New field
        caution: number;
    };

    // Identification strategy
    identifiers: string[]; // Strings to match in filename e.g. ["TEN", "텐바이텐"]

    // Parser settings
    startRow?: number; // 0-based index of first data row. Default is 1 (skipping 1 header row).
}

export interface OrderData {
    id: string; // Unique ID for key
    recipient_name: string;
    recipient_phone: string;
    zipcode: string;
    address: string;
    order_num: string;
    product_name: string;
    product_option: string;
    product_quantity: string; // New field
    caution: string;

    vendor_name: string; // Source vendor
    original_row_index: number; // For debugging
}

export type VendorConfigMap = Record<string, VendorConfig>;
