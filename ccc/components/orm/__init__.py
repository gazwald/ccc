from __future__ import annotations

from typing import Optional

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user_account"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(30))
    password: Mapped[str] = mapped_column(String(30))
    email: Mapped[Optional[str]]

    last_prompt: Mapped[Prompt] = relationship(back_populates="user")
    images: Mapped[list[Image]] = relationship(back_populates="user")


class Prompt(Base):
    __tablename__ = "prompt"
    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))
    user: Mapped[User] = relationship(back_populates="last_prompt")

    image: Mapped[Image] = relationship(back_populates="prompt")


class Image(Base):
    __tablename__ = "image"
    id: Mapped[int] = mapped_column(primary_key=True)
    tags: Mapped[list[str]] = mapped_column()

    prompt_id: Mapped[int] = mapped_column(ForeignKey("prompt.id"))
    prompt: Mapped[Prompt] = relationship(back_populates="image")

    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))
    user: Mapped[User] = relationship(back_populates="images")
