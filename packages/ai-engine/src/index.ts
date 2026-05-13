export interface AIProvider {
  name: string;
  simulate(prompt: string, context: string[]): Promise<{ score: number; reasons: string[] }>;
}

export class AIEngineRegistry {
  private providers = new Map<string, AIProvider>();
  register(provider: AIProvider) { this.providers.set(provider.name, provider); }
  get(name: string) { return this.providers.get(name); }
}
