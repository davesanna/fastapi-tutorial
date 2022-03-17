"""add content column post table

Revision ID: 3e420c73880a
Revises: fb563c0a7023
Create Date: 2022-03-17 15:00:12.254899

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "3e420c73880a"
down_revision = "fb563c0a7023"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "posts",
        sa.Column("content", sa.String(), nullable=False),
    )


def downgrade():
    op.drop_column("posts", "content")
