# CMS Adapter Contract

Required methods:
- connect(credentials)
- listContent(filters)
- createDraft(payload)
- updateContent(contentId, payload)
- publish(contentId)
- updateMetadata(contentId, metadata)
- upsertSchema(contentId, schema)
