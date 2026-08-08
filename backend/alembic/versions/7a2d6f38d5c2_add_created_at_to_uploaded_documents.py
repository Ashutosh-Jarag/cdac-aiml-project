from alembic import op
import sqlalchemy as sa

revision = "NEW_REVISION_ID"
down_revision = "ab4fc0911f2f"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "uploaded_documents",
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
    )


def downgrade():
    op.drop_column(
        "uploaded_documents",
        "created_at",
    )