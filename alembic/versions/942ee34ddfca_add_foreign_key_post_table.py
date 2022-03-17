"""add foreign key post table



Revision ID: 942ee34ddfca
Revises: 60ef8ee40e7e
Create Date: 2022-03-17 15:12:55.887110

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "942ee34ddfca"
down_revision = "60ef8ee40e7e"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("owner_id", sa.Integer(), nullable=False))
    op.create_foreign_key(
        "posts_users_fk",
        source_table="posts",
        referent_table="users",
        local_cols=["owner_id"],
        remote_cols=["id"],
        ondelete="CASCADE",
    )
    pass


def downgrade():
    op.drop_constraint("posts_users_fk", "posts")
    op.drop_column("posts", "owner_id")
