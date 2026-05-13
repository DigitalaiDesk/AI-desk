from datetime import datetime
from sqlalchemy import JSON, DateTime, ForeignKey, Integer, String, Text, Float
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class CrawlRun(Base):
    __tablename__ = "crawl_runs"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    base_url: Mapped[str] = mapped_column(String(1024), index=True)
    status: Mapped[str] = mapped_column(String(32), default="queued")
    max_pages: Mapped[int] = mapped_column(Integer, default=300)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    stats: Mapped[dict] = mapped_column(JSON, default=dict)


class CrawledPage(Base):
    __tablename__ = "crawled_pages"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    crawl_id: Mapped[int] = mapped_column(ForeignKey("crawl_runs.id"), index=True)
    url: Mapped[str] = mapped_column(String(2048), index=True)
    final_url: Mapped[str] = mapped_column(String(2048))
    status_code: Mapped[int] = mapped_column(Integer)
    depth: Mapped[int] = mapped_column(Integer)
    title: Mapped[str | None] = mapped_column(String(512), nullable=True)
    headings: Mapped[list] = mapped_column(JSON, default=list)
    metadata: Mapped[dict] = mapped_column(JSON, default=dict)
    structured_data: Mapped[list] = mapped_column(JSON, default=list)
    content: Mapped[str] = mapped_column(Text)
    canonical: Mapped[str | None] = mapped_column(String(2048), nullable=True)
    language: Mapped[str | None] = mapped_column(String(16), nullable=True)
    duplicate_hash: Mapped[str] = mapped_column(String(64), index=True)
    internal_links: Mapped[list] = mapped_column(JSON, default=list)
    fetch_ms: Mapped[float] = mapped_column(Float, default=0)


class CrawlError(Base):
    __tablename__ = "crawl_errors"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    crawl_id: Mapped[int] = mapped_column(ForeignKey("crawl_runs.id"), index=True)
    url: Mapped[str] = mapped_column(String(2048))
    error_type: Mapped[str] = mapped_column(String(128))
    message: Mapped[str] = mapped_column(Text)
    depth: Mapped[int] = mapped_column(Integer, default=0)
