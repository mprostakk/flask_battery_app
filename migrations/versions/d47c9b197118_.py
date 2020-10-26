"""empty message

Revision ID: d47c9b197118
Revises: 3caab8088315
Create Date: 2020-08-07 07:02:23.395717

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'd47c9b197118'
down_revision = '3caab8088315'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('battery', 'capacity',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('battery', 'discharge_rate',
               existing_type=postgresql.DOUBLE_PRECISION(precision=53),
               nullable=False)
    op.alter_column('battery', 'full_charge_voltage',
               existing_type=postgresql.DOUBLE_PRECISION(precision=53),
               nullable=False)
    op.alter_column('battery', 'is_active',
               existing_type=sa.BOOLEAN(),
               nullable=False)
    op.alter_column('battery', 'maintenance_voltage',
               existing_type=postgresql.DOUBLE_PRECISION(precision=53),
               nullable=False)
    op.alter_column('battery', 'min_voltage',
               existing_type=postgresql.DOUBLE_PRECISION(precision=53),
               nullable=False)
    op.alter_column('battery', 'no_of_cells',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.add_column('charge', sa.Column('charge_type', sa.Enum('charging', 'discharging', 'maintenance', name='chargestateenum'), nullable=False))
    op.alter_column('charge', 'battery_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('charge', 'start_date',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('charge', 'start_voltage',
               existing_type=postgresql.DOUBLE_PRECISION(precision=53),
               nullable=False)
    op.drop_column('charge', 'charge_tape')
    op.alter_column('charge_measurement', 'charge_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('charge_measurement', 'timestamp',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('charge_measurement', 'timestamp',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('charge_measurement', 'charge_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.add_column('charge', sa.Column('charge_tape', postgresql.ENUM('charging', 'discharging', 'maintenance', name='chargestateenum'), autoincrement=False, nullable=True))
    op.alter_column('charge', 'start_voltage',
               existing_type=postgresql.DOUBLE_PRECISION(precision=53),
               nullable=True)
    op.alter_column('charge', 'start_date',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('charge', 'battery_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.drop_column('charge', 'charge_type')
    op.alter_column('battery', 'no_of_cells',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('battery', 'min_voltage',
               existing_type=postgresql.DOUBLE_PRECISION(precision=53),
               nullable=True)
    op.alter_column('battery', 'maintenance_voltage',
               existing_type=postgresql.DOUBLE_PRECISION(precision=53),
               nullable=True)
    op.alter_column('battery', 'is_active',
               existing_type=sa.BOOLEAN(),
               nullable=True)
    op.alter_column('battery', 'full_charge_voltage',
               existing_type=postgresql.DOUBLE_PRECISION(precision=53),
               nullable=True)
    op.alter_column('battery', 'discharge_rate',
               existing_type=postgresql.DOUBLE_PRECISION(precision=53),
               nullable=True)
    op.alter_column('battery', 'capacity',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###