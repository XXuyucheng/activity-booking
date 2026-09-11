"""booking unpaid amount

Revision ID: a7f3c18e9d41
Revises: c4e8a91d2b70
Create Date: 2026-09-11 14:33:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "a7f3c18e9d41"
down_revision: Union[str, Sequence[str], None] = "c4e8a91d2b70"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "bookings",
        sa.Column("unpaid_amount", sa.Numeric(precision=10, scale=2), nullable=True),
    )
    op.execute(sa.text("UPDATE bookings SET unpaid_amount = total_price"))
    op.alter_column(
        "bookings",
        "unpaid_amount",
        existing_type=sa.Numeric(precision=10, scale=2),
        nullable=False,
    )
    op.create_check_constraint(
        "unpaid_nonneg",
        "bookings",
        "unpaid_amount >= 0",
    )
    op.create_check_constraint(
        "unpaid_lte_total",
        "bookings",
        "unpaid_amount <= total_price",
    )


def downgrade() -> None:
    op.drop_constraint(op.f("ck_bookings_unpaid_lte_total"), "bookings", type_="check")
    op.drop_constraint(op.f("ck_bookings_unpaid_nonneg"), "bookings", type_="check")
    op.drop_column("bookings", "unpaid_amount")
