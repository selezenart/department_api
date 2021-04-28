"""empty message

Revision ID: 1f66b29ef1f5
Revises: 
Create Date: 2021-04-27 16:26:16.295967

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1f66b29ef1f5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('departament',
    sa.Column('uuid', sa.String(length=16), nullable=False),
    sa.Column('title', sa.String(length=120), nullable=False),
    sa.Column('average_salary', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('uuid'),
    sa.UniqueConstraint('uuid')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('departament')
    # ### end Alembic commands ###
