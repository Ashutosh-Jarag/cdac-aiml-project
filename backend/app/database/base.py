"""
FILE CONTENTS & OVERVIEW:
-------------------------
This module serves as the central import hub and exporter for SQLAlchemy ORM database models.
It re-exports the declarative `Base` class required for model definitions, table metadata mapping, 
and Alembic database migrations.

Exports:
  - Base: Declarative base class for all database models.
"""

from app.database.connection import Base

# Explicitly define public module exports
__all__ = ["Base"]