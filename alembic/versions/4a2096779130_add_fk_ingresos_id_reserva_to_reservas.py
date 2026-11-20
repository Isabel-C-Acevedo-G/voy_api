"""add fk ingresos id_reserva to reservas

Revision ID: 4a2096779130
Revises: d46429c5e536
Create Date: 2026-11-19 19:03:25.274145

"""
from typing import Sequence, Union

from alembic import op

revision: str = "4a2096779130"
down_revision: Union[str, Sequence[str], None] = "d46429c5e536"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("ingresos", schema=None) as batch_op:
        batch_op.create_index(batch_op.f("ix_ingresos_id_reserva"), ["id_reserva"], unique=False)
        batch_op.create_foreign_key(
            "fk_ingresos_id_reserva_reservas",
            "reservas",
            ["id_reserva"],
            ["id_reserva"],
        )


def downgrade() -> None:
    with op.batch_alter_table("ingresos", schema=None) as batch_op:
        batch_op.drop_constraint("fk_ingresos_id_reserva_reservas", type_="foreignkey")
        batch_op.drop_index(batch_op.f("ix_ingresos_id_reserva"))
