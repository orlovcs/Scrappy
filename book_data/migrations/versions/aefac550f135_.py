"""empty message

Revision ID: aefac550f135
Revises: 
Create Date: 2020-05-17 16:56:33.514387

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'aefac550f135'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('books',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('author', sa.String(), nullable=True),
    sa.Column('published', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('us_infections',
    sa.Column('index', sa.Integer(), nullable=False),
    sa.Column('combined_key', sa.String(), nullable=True),
    sa.Column('date', sa.String(), nullable=True),
    sa.Column('country_region', sa.String(), nullable=True),
    sa.Column('province_state', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('index')
    )
    op.drop_index('ix_us_confirmed_index', table_name='us_confirmed')
    op.drop_table('us_confirmed')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('us_confirmed',
    sa.Column('index', sa.BIGINT(), autoincrement=False, nullable=True),
    sa.Column('uid', sa.BIGINT(), autoincrement=False, nullable=True),
    sa.Column('iso2', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('iso3', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('code3', sa.BIGINT(), autoincrement=False, nullable=True),
    sa.Column('fips', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('admin2', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('lat', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('combined_key', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('date', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('case', sa.BIGINT(), autoincrement=False, nullable=True),
    sa.Column('long', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('country/region', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('province/state', sa.TEXT(), autoincrement=False, nullable=True)
    )
    op.create_index('ix_us_confirmed_index', 'us_confirmed', ['index'], unique=False)
    op.drop_table('us_infections')
    op.drop_table('books')
    # ### end Alembic commands ###