"""Add user relationship to Donation

Revision ID: 4bf0ad6b0686
Revises: 558ee3304f24
Create Date: 2022-09-18 22:11:30.919334

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4bf0ad6b0686'
down_revision = '558ee3304f24'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('donation', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('fk_donation_user_id_user', 'user', ['user_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('donation', schema=None) as batch_op:
        batch_op.drop_constraint('fk_donation_user_id_user', type_='foreignkey')
        batch_op.drop_column('user_id')

    # ### end Alembic commands ###
