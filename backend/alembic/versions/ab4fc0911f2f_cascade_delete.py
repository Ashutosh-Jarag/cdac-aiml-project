"""cascade delete

Revision ID: ab4fc0911f2f
Revises: 8f6e7135c7d6
Create Date: 2026-08-05 18:33:01.440548
"""

from typing import Sequence, Union

from alembic import op

revision: str = "ab4fc0911f2f"
down_revision: Union[str, Sequence[str], None] = "8f6e7135c7d6"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # chat_messages -> ON DELETE CASCADE

    op.drop_constraint(
        "chat_messages_session_id_fkey",
        "chat_messages",
        type_="foreignkey",
    )

    op.create_foreign_key(
        "chat_messages_session_id_fkey",
        "chat_messages",
        "chat_sessions",
        ["session_id"],
        ["id"],
        ondelete="CASCADE",
    )

    # uploaded_documents -> ON DELETE CASCADE

    op.drop_constraint(
        "uploaded_documents_session_id_fkey",
        "uploaded_documents",
        type_="foreignkey",
    )

    op.create_foreign_key(
        "uploaded_documents_session_id_fkey",
        "uploaded_documents",
        "chat_sessions",
        ["session_id"],
        ["id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:

    op.drop_constraint(
        "chat_messages_session_id_fkey",
        "chat_messages",
        type_="foreignkey",
    )

    op.create_foreign_key(
        "chat_messages_session_id_fkey",
        "chat_messages",
        "chat_sessions",
        ["session_id"],
        ["id"],
    )

    op.drop_constraint(
        "uploaded_documents_session_id_fkey",
        "uploaded_documents",
        type_="foreignkey",
    )

    op.create_foreign_key(
        "uploaded_documents_session_id_fkey",
        "uploaded_documents",
        "chat_sessions",
        ["session_id"],
        ["id"],
    )