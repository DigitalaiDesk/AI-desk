# Agency Operating System Specification

## 1) Platform Modules

### Core Domains
1. **Client Management**
2. **Workflow Management**
3. **AI Content System**
4. **Team Collaboration**
5. **Automation System**
6. **CMS Integrations**
7. **Reporting & AI Visibility**

---

## 2) Client Management

### Entities
- `Workspace` (agency or client partition)
- `Client`
- `Project`
- `OnboardingChecklist`
- `CompetitorProfile`
- `TargetKeyword`
- `TargetEntity`
- `PromptLog`
- `ReportingSchedule`

### Required Features
- Client workspaces with data isolation
- Multi-project support per client
- Onboarding wizard (brand voice, goals, CMS credentials, analytics)
- Competitor profile registry (domain, authority, content themes)
- Target keyword/entity tracking with intent + priority
- AI prompt tracking (prompt, model, output hash, owner, outcome)
- Reporting schedules (weekly/monthly/quarterly) with recipients

### Suggested Status Model
- Onboarding: `not_started -> in_progress -> blocked -> completed`
- Projects: `planning -> active -> paused -> completed`

---

## 3) Workflow Management

### Entities
- `Pipeline`
- `Task`
- `TaskRun`
- `SOPTemplate`
- `Issue`
- `Assignee`
- `RecurrenceRule`

### Required Features
- Kanban/list/timeline task pipelines
- SOP-driven task generation
- Assignment by role/skill/capacity
- Recurring tasks for audits, reports, refreshes
- Optimization workflow types: content, technical, internal links, entities, schema
- Status tracking with SLAs and blockers

### Default Pipeline Stages
`Backlog -> Ready -> In Progress -> Review -> Approved -> Scheduled -> Published -> Measured`

---

## 4) AI Content System

### Entities
- `ContentBrief`
- `AIArticle`
- `OptimizationPass`
- `FAQSet`
- `SchemaBlock`
- `SnippetCandidate`
- `RetrievalSignal`

### Required Features
- AI article generation from brief + SERP/entity context
- SEO optimization (headings, links, topical coverage, metadata)
- AEO optimization (Q&A structure, direct answers, source clarity)
- GEO optimization (entity salience, contextual co-mentions, graph coverage)
- FAQ generation mapped to user intent stages
- Schema generation (Article, FAQPage, HowTo, Organization, Product, LocalBusiness)
- Snippet generation (title/meta/answer blocks)
- AI retrieval optimization (chunking hints, citation anchors, canonical entity naming)

### Content Lifecycle
`Brief -> Draft -> Optimize -> Fact Check -> Legal/Brand Review -> Approve -> Publish -> Monitor -> Refresh`

---

## 5) Team Collaboration

### Roles
- `Owner`
- `Admin`
- `Strategist`
- `Editor`
- `Writer`
- `SEO Analyst`
- `Developer`
- `Client Viewer`

### Permission Model
- RBAC with per-workspace overrides
- Object-level permissions for projects and tasks
- Approval gates by content risk level

### Required Features
- Threaded comments on tasks/content/audits
- Mentions and task assignments
- Notifications (in-app + email + digest)
- Approval system with required reviewers and due dates

---

## 6) Automation System

### Required Features
- Recurring crawls per project/site segment
- Automated report compilation and delivery
- Automated recommendation engine from crawl/content/ranking deltas
- AI-assisted fixes with human approval gates
- Content scheduling calendar with channel/CMS targeting

### Automation Rules Engine
Rule format:
- Trigger (`schedule`, `status_change`, `metric_threshold`, `webhook`)
- Conditions
- Actions (`create_task`, `run_audit`, `generate_content`, `notify`, `publish`)

---

## 7) CMS Integrations

### Supported Platforms
- WordPress
- Shopify
- Webflow
- Wix

### Integration Capabilities
- Publish drafts and updates
- Metadata updates (title/meta/OG/canonical)
- Schema injection/updates
- On-page optimization updates

### Adapter Interface
Each CMS adapter should expose:
- `connect(credentials)`
- `listContent(filters)`
- `createDraft(payload)`
- `updateContent(contentId, payload)`
- `publish(contentId)`
- `updateMetadata(contentId, metadata)`
- `upsertSchema(contentId, schema)`

---

## 8) Reporting & AI Visibility Optimization

### Dashboards
- SEO performance (rankings, traffic, conversions)
- AEO performance (answer inclusion, assistant-style response match)
- GEO performance (entity coverage and prominence)
- AI visibility score by topic/entity/query class

### Recurring Audits
- Technical audit
- Content quality/comprehensiveness audit
- Internal linking audit
- Schema validity audit
- AI retrieval/readability audit

### Report Artifacts
- Executive summary
- Wins/losses since prior period
- Priority actions with owners/dates
- Forecast and confidence

---

## 9) Minimal Data Model (starter)

```text
Workspace 1---* Client 1---* Project 1---* Pipeline 1---* Task
Project 1---* CompetitorProfile
Project 1---* TargetKeyword
Project 1---* TargetEntity
Project 1---* ContentBrief 1---* AIArticle 1---* OptimizationPass
Project 1---* PromptLog
Project 1---* ReportingSchedule
Task 1---* Comment
Task *---1 User (assignee)
```

---

## 10) API Surface (starter)

### Client + Project
- `POST /workspaces`
- `POST /clients`
- `POST /projects`
- `POST /projects/{id}/onboarding`
- `POST /projects/{id}/competitors`
- `POST /projects/{id}/keywords`
- `POST /projects/{id}/entities`

### Workflow
- `POST /pipelines`
- `POST /tasks`
- `POST /tasks/{id}/assign`
- `POST /tasks/{id}/status`
- `POST /sop-templates`
- `POST /recurrence-rules`

### AI Content
- `POST /content/briefs`
- `POST /content/generate-article`
- `POST /content/optimize/seo`
- `POST /content/optimize/aeo`
- `POST /content/optimize/geo`
- `POST /content/generate-faq`
- `POST /content/generate-schema`
- `POST /content/generate-snippets`

### Automation + Reporting
- `POST /automations/rules`
- `POST /automations/run`
- `POST /audits/schedule`
- `POST /reports/schedule`
- `POST /reports/run`

### CMS
- `POST /integrations/{cms}/connect`
- `POST /integrations/{cms}/publish`
- `POST /integrations/{cms}/metadata`
- `POST /integrations/{cms}/schema`

---

## 11) Delivery Roadmap

### Phase 1 (MVP)
- Workspaces, clients, projects, tasks, RBAC
- AI drafting + SEO optimization
- WordPress publishing
- Weekly reporting

### Phase 2
- AEO/GEO scoring + retrieval optimization
- Shopify/Webflow adapters
- automation rules engine + recurring crawls

### Phase 3
- Wix adapter
- predictive recommendations
- cross-client benchmarking and portfolio analytics
