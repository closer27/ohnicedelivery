import ExcelJS from "exceljs";
import * as XLSX from "xlsx";
import { OrderData, VendorConfig, VendorConfigMap } from "@/types";

export const EXCEL_MIME_TYPES = [
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "application/vnd.ms-excel",
    "text/csv",
];

export async function readExcelFile(file: File): Promise<any[][]> {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = (e) => {
            try {
                const data = e.target?.result;
                const workbook = XLSX.read(data, { type: "array" });
                const firstSheetName = workbook.SheetNames[0];
                const worksheet = workbook.Sheets[firstSheetName];
                const jsonData = XLSX.utils.sheet_to_json(worksheet, { header: 1 });
                resolve(jsonData as any[][]);
            } catch (err) {
                reject(err);
            }
        };
        reader.onerror = (err) => reject(err);
        reader.readAsArrayBuffer(file);
    });
}

export function detectVendor(filename: string, vendors: VendorConfigMap): string | null {
    const normalizedName = filename.normalize("NFC"); // Normalize unicode

    for (const [id, config] of Object.entries(vendors)) {
        for (const identifier of config.identifiers) {
            if (normalizedName.includes(identifier)) {
                return id;
            }
        }
    }
    return null;
}

export function mapRowToOrder(
    row: any[],
    vendor: VendorConfig,
    rowIndex: number
): OrderData {
    const m = vendor.mappings;

    // Helper to safely get string value
    const getVal = (idx: number) => {
        const val = row[idx];
        return val !== undefined && val !== null ? String(val).trim() : "";
    };

    return {
        id: `${vendor.id}-${rowIndex}`,
        vendor_name: vendor.name,
        original_row_index: rowIndex,
        recipient_name: getVal(m.recipient_name),
        recipient_phone: getVal(m.recipient_phone),
        zipcode: getVal(m.zipcode),
        address: getVal(m.address),
        order_num: getVal(m.order_num),
        product_name: getVal(m.product_name),
        product_option: getVal(m.product_option),
        product_quantity: getVal(m.product_quantity),
        caution: getVal(m.caution),
    };
}

export async function generateUnifiedExcel(orders: OrderData[]): Promise<Uint8Array> {
    const workbook = new ExcelJS.Workbook();
    const worksheet = workbook.addWorksheet("Sheet1");

    // Legacy Styles
    // Font: Malgun Gothic, 11pt (size 11)
    // Header BG: 0xCFEED1 -> ARGB FFCFEED1 ? Actually xlwt uses closest system color usually, but we use hex.
    // Legacy: 207, 238, 209 -> #CFEED1
    // Header Font Color: 43, 95, 24 -> #2B5F18
    // Align: vert center, wrap

    // Define Columns with Widths (256 * N in xlwt usually approximates N chars, exceljs uses width units ~ chars)
    // Legacy:
    // Col 0 (Recipient): 256 * 7 -> ~7
    // Col 1 (Zipcode): 256 * 18 -> ~18
    // Col 2 (Address): 256 * 69 -> ~69
    // Col 3 (Phone): 256 * 18 -> ~18
    // Col 4 (Contact2): 256 * 18 -> ~18
    // Col 5 (ProductStr): 256 * 61 -> ~61
    // Col 6 (Msg): 256 * 11 -> ~11
    // Col 7 (Quantity): 256 * 61 (Referencing 'Reference' col width from legacy?) Let's matches others.

    worksheet.columns = [
        { width: 7 },  // Recipient
        { width: 18 }, // Zipcode
        { width: 69 }, // Address
        { width: 18 }, // Phone
        { width: 18 }, // Contact 2
        { width: 61 }, // Product String
        { width: 11 }, // Message
        { width: 11 }, // Quantity (H)
        { width: 57 }, // Option (I) - Updated to 57
    ];

    // Header Row
    const headerTexts = [
        "수령인",
        "우편번호(생략가능)",
        "전체 주소",
        "연락처1\n(예) 0505-780-0505",
        "연락처2\n(예) 010-2879-6266",
        "상품명 (alt+enter 꼭 줄바꿈으로 구분할것, 독립된 셀에 적지마세요)\n(예) 김미진_무광하드_아이폰7_1개\n(예) 이진영_무광터프_아이폰7_3개",
        "배송메세지",
        "", // Quantity (Requested empty)
        "", // Option (Requested empty)
    ];

    const headerRow = worksheet.getRow(1);
    headerRow.values = headerTexts;
    headerRow.height = 54;

    headerRow.eachCell((cell, colNumber) => {
        cell.font = {
            name: "Malgun Gothic",
            size: 11,
            color: { argb: "FF2B5F18" }, // #2B5F18
        };

        // Skip background color for Cols H (8) and I (9)
        if (colNumber !== 8 && colNumber !== 9) {
            cell.fill = {
                type: "pattern",
                pattern: "solid",
                fgColor: { argb: "FFCFEED1" }, // #CFEED1
            };
        }

        cell.alignment = {
            vertical: "middle",
            wrapText: true,
            horizontal: "center",
        };
    });

    // Data Rows
    orders.forEach((o, index) => {
        // [위탁][패키지][사은품1]{Option}_1개
        const constructedProduct = `[위탁][패키지][사은품1]${o.product_option}_1개`;

        // Format Quantity: append '개' if exists
        const quantityStr = o.product_quantity ? `${o.product_quantity}개` : "";

        const rowValues = [
            o.recipient_name,
            o.zipcode,
            o.address,
            o.recipient_phone,
            "", // Contact 2
            constructedProduct,
            o.caution,
            quantityStr,       // Quantity with '개'
            o.product_name     // Col I: Product Name (Previously Option)
        ];

        const row = worksheet.addRow(rowValues);
        row.height = 90; // Legacy 90*20 units -> 90pt.

        row.eachCell((cell) => {
            cell.font = {
                name: "Malgun Gothic",
                size: 11,
            };
            cell.alignment = {
                vertical: "middle",
                wrapText: true,
            };
        });
    });

    const buffer = await workbook.xlsx.writeBuffer();
    return new Uint8Array(buffer);
}
