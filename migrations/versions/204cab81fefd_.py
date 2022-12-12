"""empty message

Revision ID: 204cab81fefd
Revises: 2a38e35c07bb
Create Date: 2022-12-12 02:57:37.723235

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '204cab81fefd'
down_revision = '2a38e35c07bb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('current_activation_jwt', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('current_password_jwt', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('current_password_jwt')
        batch_op.drop_column('current_activation_jwt')

    # ### end Alembic commands ###