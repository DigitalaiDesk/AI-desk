import type { ScoreBundle } from '@ai-desk/types';

export function computeCompositeScore(scores: ScoreBundle): number {
  return Number(((scores.seoScore + scores.aiVisibilityScore + scores.retrievalReadinessScore + scores.citationProbabilityScore) / 4).toFixed(2));
}
