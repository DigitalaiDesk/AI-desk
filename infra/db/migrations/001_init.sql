CREATE TABLE IF NOT EXISTS domains (
  id UUID PRIMARY KEY,
  domain TEXT UNIQUE NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS crawl_pages (
  id UUID PRIMARY KEY,
  domain_id UUID REFERENCES domains(id),
  url TEXT NOT NULL,
  html TEXT,
  status_code INTEGER,
  crawled_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS entity_mentions (
  id UUID PRIMARY KEY,
  page_id UUID REFERENCES crawl_pages(id),
  entity_name TEXT NOT NULL,
  entity_type TEXT,
  confidence REAL,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
