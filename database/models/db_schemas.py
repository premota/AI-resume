from datetime import datetime
from database.base import Base

from sqlalchemy import DateTime, UniqueConstraint, func
from sqlalchemy import String, JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class UserTable(Base):
    __tablename__ = "User_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(254), unique=True)
    username: Mapped[str] = mapped_column(String(30))
    password: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    cvs: Mapped[list["CVTable"]] = relationship(
        "CVTable", back_populates="user", cascade="all, delete-orphan"
    )
    jds: Mapped[list["JDTable"]] = relationship(
        "JDTable", back_populates="user", cascade="all, delete-orphan"
    )


class CVTable(Base):
    __tablename__ = "CV_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("User_table.id"))
    cv_hash: Mapped[str] = mapped_column(
        String(64), unique=True, nullable=False, index=True
    )
    cv_content: Mapped[dict] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    user: Mapped["UserTable"] = relationship("UserTable", back_populates="cvs")
    matches: Mapped[list["Matched"]] = relationship(
        "Matched", back_populates="cv", cascade="all, delete-orphan"
    )


class JDTable(Base):
    __tablename__ = "JD_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("User_table.id"))
    jd_hash: Mapped[str] = mapped_column(
        String(64), unique=True, nullable=False, index=True
    )
    jd_content: Mapped[dict] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    user: Mapped["UserTable"] = relationship("UserTable", back_populates="jds")
    matches: Mapped[list["Matched"]] = relationship(
        "Matched", back_populates="jd"
    )


class Matched(Base):
    __tablename__ = "Matched"

    id: Mapped[int] = mapped_column(primary_key=True)
    cv_id: Mapped[int] = mapped_column(ForeignKey("CV_table.id"), nullable=False)
    jd_id: Mapped[int] = mapped_column(ForeignKey("JD_table.id"), nullable=False)
    score: Mapped[float] = mapped_column(nullable=False, index=True)
    matched_content: Mapped[dict] = mapped_column(JSON, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    cv: Mapped["CVTable"] = relationship("CVTable", back_populates="matches")
    jd: Mapped["JDTable"] = relationship("JDTable", back_populates="matches")

    __table_args__ = (
        UniqueConstraint("cv_id", "jd_id", name="uq_cv_jd_match"),
    )