export function logInfo(message: string, context?: Record<string, unknown>) {
  console.info(`[AI-desk] ${message}`, context ?? {});
}
