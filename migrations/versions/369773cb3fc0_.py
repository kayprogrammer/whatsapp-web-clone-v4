"""empty message

Revision ID: 369773cb3fc0
Revises: d05edc97acd8
Create Date: 2022-12-16 23:09:57.458709

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '369773cb3fc0'
down_revision = 'd05edc97acd8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('tz_id', sa.Integer(), nullable=True))
        batch_op.drop_constraint('user_tz_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'timezone', ['tz_id'], ['pkid'], ondelete='SET NULL')
        batch_op.drop_column('tz')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('tz', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('user_tz_fkey', 'timezone', ['tz'], ['pkid'])
        batch_op.drop_column('tz_id')

    # ### end Alembic commands ###
