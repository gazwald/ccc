from __future__ import annotations

from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.types import JSON, Interval, String


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)


class User(Base):
    __tablename__ = "user_account"
    username: Mapped[str] = mapped_column(String(30))
    password: Mapped[str] = mapped_column(String(30))
    email: Mapped[Optional[str]]

    last_prompt: Mapped[Prompt] = relationship(back_populates="user")
    images: Mapped[list[Image]] = relationship(back_populates="user")


class Prompt(Base):
    __tablename__ = "prompt"
    prompt: Mapped[dict] = mapped_column(JSON)
    processing_duration: Mapped[Interval]

    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))
    user: Mapped[User] = relationship(back_populates="last_prompt")

    image: Mapped[Image] = relationship(back_populates="prompt")


class Image(Base):
    __tablename__ = "image"
    image: Mapped[str]

    prompt_id: Mapped[int] = mapped_column(ForeignKey("prompt.id"))
    prompt: Mapped[Prompt] = relationship(back_populates="image")

    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))
    user: Mapped[User] = relationship(back_populates="images")
