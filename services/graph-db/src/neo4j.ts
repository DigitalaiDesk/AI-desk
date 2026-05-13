export class Neo4jAdapter {
  async mergeEntity(entity: string, type: string) {
    return { entity, type, merged: true };
  }
}
