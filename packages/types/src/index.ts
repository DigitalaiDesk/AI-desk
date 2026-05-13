export type ScoreBundle = {
  seoScore: number;
  aiVisibilityScore: number;
  retrievalReadinessScore: number;
  citationProbabilityScore: number;
};

export interface CrawlPage {
  url: string;
  content: string;
}
