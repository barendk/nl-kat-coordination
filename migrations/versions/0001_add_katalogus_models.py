"""Add KATalogus models.

Revision ID: 0001
Revises: 
Create Date: 2022-05-18 14:19:15.882901

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "organisation",
        sa.Column("pk", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("id", sa.String(length=4), nullable=False),
        sa.Column("name", sa.String(length=64), nullable=False),
        sa.PrimaryKeyConstraint("pk"),
    )
    op.create_table(
        "repository",
        sa.Column("pk", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("id", sa.String(length=32), nullable=False),
        sa.Column("name", sa.String(length=64), nullable=False),
        sa.Column("base_url", sa.String(length=128), nullable=False),
        sa.PrimaryKeyConstraint("pk"),
    )
    op.create_table(
        "organisation_repository",
        sa.Column("organisation_pk", sa.Integer(), nullable=False),
        sa.Column("repository_pk", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["organisation_pk"],
            ["organisation.pk"],
        ),
        sa.ForeignKeyConstraint(
            ["repository_pk"],
            ["repository.pk"],
        ),
    )
    op.create_table(
        "setting",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("key", sa.String(length=32), nullable=False),
        sa.Column("value", sa.String(length=64), nullable=False),
        sa.Column("organisation_pk", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["organisation_pk"], ["organisation.pk"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "plugin_state",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("plugin_id", sa.String(length=32), nullable=False),
        sa.Column("enabled", sa.Boolean(), nullable=False),
        sa.Column("organisation_pk", sa.Integer(), nullable=False),
        sa.Column("repository_pk", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["organisation_pk"], ["organisation.pk"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["repository_pk"], ["repository.pk"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("plugin_id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("plugin_state")
    op.drop_table("setting")
    op.drop_table("organisation_repository")
    op.drop_table("repository")
    op.drop_table("organisation")
    # ### end Alembic commands ###
