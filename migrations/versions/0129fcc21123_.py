"""empty message

Revision ID: 0129fcc21123
Revises: 550a4e42725b
Create Date: 2017-06-15 06:17:11.576239

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '0129fcc21123'
down_revision = '550a4e42725b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('flights', sa.Column('flight_no', sa.String(length=60), nullable=True))
    op.add_column('flights', sa.Column('from_airport', sa.String(length=60), nullable=True))
    op.add_column('flights', sa.Column('to_airport', sa.String(length=60), nullable=True))
    op.drop_index('name', table_name='flights')
    op.create_unique_constraint(None, 'flights', ['flight_no'])
    op.drop_column('flights', 'description')
    op.drop_column('flights', 'name')
    op.drop_index('name', table_name='insurances')
    op.drop_column('insurances', 'name')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('insurances', sa.Column('name', mysql.VARCHAR(length=60), nullable=True))
    op.create_index('name', 'insurances', ['name'], unique=True)
    op.add_column('flights', sa.Column('name', mysql.VARCHAR(length=60), nullable=True))
    op.add_column('flights', sa.Column('description', mysql.VARCHAR(length=200), nullable=True))
    op.drop_constraint(None, 'flights', type_='unique')
    op.create_index('name', 'flights', ['name'], unique=True)
    op.drop_column('flights', 'to_airport')
    op.drop_column('flights', 'from_airport')
    op.drop_column('flights', 'flight_no')
    # ### end Alembic commands ###
