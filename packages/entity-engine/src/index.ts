export interface EntityMention { entity: string; type: string; confidence: number; }
export interface EntityExtractor { extract(text: string): Promise<EntityMention[]>; }
