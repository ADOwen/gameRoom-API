"""empty message

Revision ID: 194c95654ee5
Revises: 4d13fba5e628
Create Date: 2022-02-02 22:25:40.719758

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '194c95654ee5'
down_revision = '4d13fba5e628'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('post', 'username',
               existing_type=sa.VARCHAR(length=150),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('post', 'username',
               existing_type=sa.VARCHAR(length=150),
               nullable=True)
    # ### end Alembic commands ###
