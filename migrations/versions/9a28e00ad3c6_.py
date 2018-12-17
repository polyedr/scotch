"""empty message

Revision ID: 9a28e00ad3c6
Revises: becc83247a44
Create Date: 2018-12-17 14:16:51.051828

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9a28e00ad3c6'
down_revision = 'becc83247a44'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=256), nullable=False),
    sa.Column('password', sa.String(length=256), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.add_column('bucketlists', sa.Column('created_by', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'bucketlists', 'users', ['created_by'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'bucketlists', type_='foreignkey')
    op.drop_column('bucketlists', 'created_by')
    op.drop_table('users')
    # ### end Alembic commands ###