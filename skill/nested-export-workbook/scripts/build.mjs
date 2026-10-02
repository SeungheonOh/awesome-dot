import fs from 'node:fs/promises';
import path from 'node:path';
import { SpreadsheetFile, Workbook } from '@oai/artifact-tool';

const [planFile, destination] = process.argv.slice(2);
if (!destination) {
  throw new Error('Usage: node build.mjs plan.json destination.xlsx');
}
const plan = JSON.parse(await fs.readFile(planFile, 'utf8'));
const column = n => {
  let value = '';
  while (n) { const r = (n - 1) % 26; value = String.fromCharCode(65 + r) + value; n = Math.floor((n - 1) / 26); }
  return value;
};
// The author's documented literal-text API consumes this one quote. Saved-file
// checks demand the original value without a quote and with no formula node.
const literal = value => typeof value === 'string' && value.startsWith('=') ? "'" + value : value;
const widths = {
  Collections: [12, 30, 20, 16, 17, 17, 13, 17, 13, 23],
  Items: [13, 12, 28, 18, 12, 18, 17, 17, 29, 23],
  Labels: [13, 12, 26, 31, 25],
  'Source paths': [12, 40, 30, 16, 18, 45, 27]
};
let workbook;
{
  await fs.mkdir(path.dirname(destination), { recursive: true });
  // Refuse accidental replacement of a previous deliverable.
  try { await fs.access(destination); throw new Error('Destination already exists'); }
  catch (e) { if (e.code !== 'ENOENT') throw e; }
  workbook = Workbook.create();
  for (const name of Object.keys(plan.headers)) {
    const sheet = workbook.worksheets.add(name);
    const matrix = [plan.headers[name], ...plan.rows[name]].map(row => row.map(literal));
    const last = column(matrix[0].length);
    const range = sheet.getRange(`A1:${last}${matrix.length}`);
    range.format.numberFormat = '@';
    range.values = matrix;
    range.format.font = { name: 'Arial', size: 10, color: '#202936' };
    range.format.rowHeight = 25;
    range.format.verticalAlignment = 'center';
    range.format.horizontalAlignment = 'left';
    range.format.wrapText = false;
    for (let c = 0; c < widths[name].length; c++) {
      sheet.getRange(`${column(c + 1)}1:${column(c + 1)}${matrix.length}`).format.columnWidth = widths[name][c];
    }
    // Numeric ordinals, counts and quantities remain native numbers. String
    // identifiers and date-looking strings remain explicit text.
    for (let r = 1; r < matrix.length; r++) {
      for (let c = 0; c < matrix[r].length; c++) {
        if (typeof matrix[r][c] === 'number') {
          sheet.getCell(r, c).format.numberFormat = '0';
          sheet.getCell(r, c).format.horizontalAlignment = 'center';
        }
      }
    }
    const table = sheet.tables.add(`A1:${last}${matrix.length}`, true, name.replaceAll(' ', '') + 'Data');
    table.showFilterButton = true;
    table.style = 'TableStyleMedium2';
    sheet.getRange(`A1:${last}1`).format = {
      fill: '#24374A', font: { name: 'Arial', size: 10, bold: true, color: '#FFFFFF' },
      rowHeight: 29, horizontalAlignment: 'center', verticalAlignment: 'center'
    };
    sheet.showGridLines = false;
    sheet.freezePanes.freezeRows(1);
    sheet.freezePanes.freezeColumns(name === 'Source paths' ? 2 : 1);
  }
  const read = workbook.worksheets.add('Read me');
  const notes = [
    ['Nested export workbook', null],
    ['Source file', plan.source.file],
    ['Source bytes', plan.source.bytes],
    ['Source SHA-256', plan.source.sha256],
    ['Selection', plan.source.selection],
    ['Source format', plan.source.format],
    ['Exported at (JSON text)', JSON.stringify(plan.source.exportedAt)],
    ['Row identity', 'Use source pointers, not names or business IDs. All order columns are zero-based.'],
    ['Relationships', 'Items and Labels are separate child tables. Join by Parent pointer; never multiply sibling arrays.'],
    ['Blank cells', 'Read the paired state. EMPTY_STRING is supplied ""; NULL is explicit null; MISSING is absent.'],
    ['Child arrays', 'EMPTY_ARRAY is supplied []; ARRAY has ordered children. NULL and MISSING have no child rows.'],
    ['Source paths', 'Every actual JSON node is listed in source traversal order. Extra MISSING rows are schema observations, not source nodes.'],
    ['Root pointer', 'The JSON document root is the empty pointer. Scalar JSON preserves each scalar as an inert JSON token.'],
    ['Numbers and dates', 'Quantity is a native integer when present. IDs and timestamp/date-looking strings remain text.'],
    ['Review edits', 'This is a static conversion. Editing a value does not update lineage or state. Regenerate from the unchanged source.'],
    ['Scope', 'Internal conversion fidelity only. No claim about account completeness, Excel or a cloud application.']
  ];
  read.getRange('A1:B16').format.numberFormat = '@';
  read.getRange('A1:B16').values = notes.map(row => row.map(literal));
  read.getRange('B3').format.numberFormat = '0';
  read.getRange('A1:B16').format.font = { name: 'Arial', size: 10, color: '#202936' };
  read.getRange('A1:B16').format.verticalAlignment = 'center';
  read.getRange('A1:A16').format.columnWidth = 27;
  read.getRange('B1:B16').format.columnWidth = 100;
  read.getRange('A1:B16').format.rowHeight = 32;
  read.getRange('B1:B16').format.wrapText = true;
  read.getRange('A1').format.font = { name: 'Arial', size: 14, bold: true, color: '#24374A' };
  read.getRange('A2:A16').format.font.bold = true;
  read.getRange('A1:B1').format.rowHeight = 36;
  read.getRange('A8:B16').format.rowHeight = 42;
  read.showGridLines = false;
  workbook.recalculate();
  const inspection = await workbook.inspect({ kind: 'table', range: 'Items!A1:J5', include: 'values,formulas', maxChars: 4500, tableMaxRows: 5, tableMaxCols: 10 });
  console.log(inspection.ndjson);
  const formulaScan = await workbook.inspect({ kind: 'formula', maxChars: 1000, options: { maxResults: 10 } });
  console.log(formulaScan.ndjson);
  const xlsx = await SpreadsheetFile.exportXlsx(workbook);
  await xlsx.save(destination);
}
