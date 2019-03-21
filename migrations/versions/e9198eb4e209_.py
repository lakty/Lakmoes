"""empty message

Revision ID: e9198eb4e209
Revises: 903f5d45a075
Create Date: 2019-03-21 22:29:07.362528

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e9198eb4e209'
down_revision = '903f5d45a075'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('connects',
    sa.Column('fk_record_from', sa.Integer(), nullable=False),
    sa.Column('fk_record_to', sa.Integer(), nullable=False),
    sa.Column('category_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['category.id'], ),
    sa.ForeignKeyConstraint(['fk_record_from'], ['record.id'], ),
    sa.ForeignKeyConstraint(['fk_record_to'], ['record.id'], ),
    sa.PrimaryKeyConstraint('fk_record_from', 'fk_record_to')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('connects')
    # ### end Alembic commands ###