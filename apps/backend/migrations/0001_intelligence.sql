CREATE TABLE IF NOT EXISTS crawl_runs (
  id SERIAL PRIMARY KEY,
  base_url VARCHAR(1024) NOT NULL,
  status VARCHAR(32) NOT NULL DEFAULT 'queued',
  max_pages INT NOT NULL DEFAULT 300,
  created_at TIMESTAMP NOT NULL DEFAULT NOW(),
  completed_at TIMESTAMP NULL,
  stats JSONB NOT NULL DEFAULT '{}'::jsonb
);
CREATE TABLE IF NOT EXISTS crawled_pages (
  id SERIAL PRIMARY KEY,
  crawl_id INT NOT NULL REFERENCES crawl_runs(id),
  url VARCHAR(2048) NOT NULL,
  final_url VARCHAR(2048) NOT NULL,
  status_code INT NOT NULL,
  depth INT NOT NULL,
  title VARCHAR(512),
  headings JSONB NOT NULL DEFAULT '[]'::jsonb,
  metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
  structured_data JSONB NOT NULL DEFAULT '[]'::jsonb,
  content TEXT NOT NULL,
  canonical VARCHAR(2048),
  language VARCHAR(16),
  duplicate_hash VARCHAR(64) NOT NULL,
  internal_links JSONB NOT NULL DEFAULT '[]'::jsonb,
  fetch_ms DOUBLE PRECISION NOT NULL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS crawl_errors (
  id SERIAL PRIMARY KEY,
  crawl_id INT NOT NULL REFERENCES crawl_runs(id),
  url VARCHAR(2048) NOT NULL,
  error_type VARCHAR(128) NOT NULL,
  message TEXT NOT NULL,
  depth INT NOT NULL DEFAULT 0
);
