export type ReportFormat = 'json' | 'html';
export function generateReport(payload: unknown, format: ReportFormat): string {
  if (format === 'json') return JSON.stringify(payload, null, 2);
  return `<pre>${JSON.stringify(payload, null, 2)}</pre>`;
}
