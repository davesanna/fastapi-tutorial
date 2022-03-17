"""create posts table

Revision ID: fb563c0a7023
Revises: 
Create Date: 2022-03-17 14:01:00.989818

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "fb563c0a7023"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "posts",
        sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("title", sa.String(), nullable=False),
    )
    pass


def downgrade():
    op.drop_table("posts")
    pass
