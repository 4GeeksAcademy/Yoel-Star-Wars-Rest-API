"""empty message

Revision ID: 565c7e65e57f
Revises: 465571847fc5
Create Date: 2024-01-09 12:27:23.475156

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '565c7e65e57f'
down_revision = '465571847fc5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('association', schema=None) as batch_op:
        batch_op.alter_column('planet_id',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('character_id',
               existing_type=sa.INTEGER(),
               nullable=True)

    with op.batch_alter_table('character', schema=None) as batch_op:
        batch_op.create_unique_constraint(None, ['id'])

    with op.batch_alter_table('planet', schema=None) as batch_op:
        batch_op.create_unique_constraint(None, ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('planet', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')

    with op.batch_alter_table('character', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')

    with op.batch_alter_table('association', schema=None) as batch_op:
        batch_op.alter_column('character_id',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('planet_id',
               existing_type=sa.INTEGER(),
               nullable=False)

    # ### end Alembic commands ###
