"""add age column

Revision ID: 848297f61ba6
Revises: 62ea5c8dd929
Create Date: 2022-06-12 10:01:29.059477

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '848297f61ba6'
down_revision = '62ea5c8dd929'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('age', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('age')

    # ### end Alembic commands ###
