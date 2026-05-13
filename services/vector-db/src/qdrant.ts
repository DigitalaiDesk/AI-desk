export interface VectorPoint { id: string; vector: number[]; payload?: Record<string, unknown>; }
export class QdrantAdapter {
  async upsert(collection: string, points: VectorPoint[]): Promise<{ collection: string; count: number }> {
    return { collection, count: points.length };
  }
}
