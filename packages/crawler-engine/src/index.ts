export interface CrawlResult { urls: string[]; }
export interface Crawler { crawl(seedUrl: string, limit: number): Promise<CrawlResult>; }
