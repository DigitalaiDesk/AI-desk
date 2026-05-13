export class LocalModelRuntime {
  async generate(model: string, prompt: string): Promise<string> {
    return `[${model}] ${prompt.slice(0, 200)}`;
  }
}
