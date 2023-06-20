"""Add job table

Revision ID: 0008
Revises: 0007
Create Date: 2023-06-15 14:25:58.433935

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

import scheduler

# revision identifiers, used by Alembic.
revision = "0008"
down_revision = "0007"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "jobs",
        sa.Column("id", scheduler.utils.datastore.GUID(), nullable=False),
        sa.Column("scheduler_id", sa.String(), nullable=True),
        sa.Column("hash", sa.String(length=32), nullable=True),
        sa.Column("enabled", sa.Boolean(), nullable=True),
        sa.Column("crontab", sa.String(), nullable=True),
        sa.Column("p_item", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("deadline", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=True),
        sa.Column("evaluated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("modified_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_jobs_hash"), "jobs", ["hash"], unique=False)
    op.add_column("tasks", sa.Column("job_id", scheduler.utils.datastore.GUID(), nullable=True))
    op.create_foreign_key(None, "tasks", "jobs", ["job_id"], ["id"])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "tasks", type_="foreignkey")
    op.drop_column("tasks", "job_id")
    op.drop_index(op.f("ix_jobs_hash"), table_name="jobs")
    op.drop_table("jobs")
    # ### end Alembic commands ###
