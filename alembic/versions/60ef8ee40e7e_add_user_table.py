"""add user table

Revision ID: 60ef8ee40e7e
Revises: 3e420c73880a
Create Date: 2022-03-17 15:04:29.884483

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "60ef8ee40e7e"
down_revision = "3e420c73880a"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    pass


def downgrade():
    op.drop_table("users")
    pass
