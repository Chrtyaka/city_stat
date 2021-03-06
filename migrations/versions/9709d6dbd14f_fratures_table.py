"""fratures table

Revision ID: 9709d6dbd14f
Revises: 
Create Date: 2018-05-02 02:33:46.226488

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9709d6dbd14f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('category',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('categoryname', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('country',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('countryname', sa.String(length=64), nullable=True),
    sa.Column('coordinates', sa.String(length=5000), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('group',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('groupname', sa.String(length=64), nullable=True),
    sa.Column('group', sa.String(length=64), nullable=True),
    sa.Column('coordinates', sa.String(length=5000), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('feature',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('featurename', sa.String(length=64), nullable=True),
    sa.Column('category_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['category.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('province',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('provincename', sa.String(length=64), nullable=True),
    sa.Column('coordinates', sa.String(length=5000), nullable=True),
    sa.Column('country_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['country_id'], ['country.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('area',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('areaname', sa.String(length=64), nullable=True),
    sa.Column('coordinates', sa.String(length=5000), nullable=True),
    sa.Column('province_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['province_id'], ['province.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('feature_country',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('country_id', sa.Integer(), nullable=True),
    sa.Column('feature_id', sa.Integer(), nullable=True),
    sa.Column('value', sa.String(length=64), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['country_id'], ['country.id'], ),
    sa.ForeignKeyConstraint(['feature_id'], ['feature.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('feature_province',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('province_id', sa.Integer(), nullable=True),
    sa.Column('feature_id', sa.Integer(), nullable=True),
    sa.Column('value', sa.String(length=64), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['feature_id'], ['feature.id'], ),
    sa.ForeignKeyConstraint(['province_id'], ['province.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('group_province',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('group_id', sa.Integer(), nullable=True),
    sa.Column('province_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['group_id'], ['group.id'], ),
    sa.ForeignKeyConstraint(['province_id'], ['province.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('feature_area',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('area_id', sa.Integer(), nullable=True),
    sa.Column('feature_id', sa.Integer(), nullable=True),
    sa.Column('value', sa.String(length=64), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['area_id'], ['area.id'], ),
    sa.ForeignKeyConstraint(['feature_id'], ['feature.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('locality',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('localityname', sa.String(length=64), nullable=True),
    sa.Column('coordinates', sa.String(length=5000), nullable=True),
    sa.Column('province_id', sa.Integer(), nullable=True),
    sa.Column('area_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['area_id'], ['area.id'], ),
    sa.ForeignKeyConstraint(['province_id'], ['province.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('district',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('districtname', sa.String(length=64), nullable=True),
    sa.Column('coordinates', sa.String(length=5000), nullable=True),
    sa.Column('locality_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['locality_id'], ['locality.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('feature_locality',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('locality_id', sa.Integer(), nullable=True),
    sa.Column('feature_id', sa.Integer(), nullable=True),
    sa.Column('value', sa.String(length=64), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['feature_id'], ['feature.id'], ),
    sa.ForeignKeyConstraint(['locality_id'], ['locality.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('street',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('streetname', sa.String(length=64), nullable=True),
    sa.Column('coordinates', sa.String(length=5000), nullable=True),
    sa.Column('locality_id', sa.Integer(), nullable=True),
    sa.Column('fias_id', sa.String(length=64), nullable=True),
    sa.ForeignKeyConstraint(['locality_id'], ['locality.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_street_fias_id'), 'street', ['fias_id'], unique=True)
    op.create_table('address',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('country_id', sa.Integer(), nullable=True),
    sa.Column('province_id', sa.Integer(), nullable=True),
    sa.Column('area_id', sa.Integer(), nullable=True),
    sa.Column('locality_id', sa.Integer(), nullable=True),
    sa.Column('district_id', sa.Integer(), nullable=True),
    sa.Column('street_id', sa.Integer(), nullable=True),
    sa.Column('house', sa.String(length=10), nullable=True),
    sa.Column('block', sa.String(length=10), nullable=True),
    sa.Column('building', sa.String(length=10), nullable=True),
    sa.Column('postcode', sa.String(length=10), nullable=True),
    sa.Column('addressline', sa.String(length=64), nullable=True),
    sa.ForeignKeyConstraint(['area_id'], ['area.id'], ),
    sa.ForeignKeyConstraint(['country_id'], ['country.id'], ),
    sa.ForeignKeyConstraint(['district_id'], ['district.id'], ),
    sa.ForeignKeyConstraint(['locality_id'], ['locality.id'], ),
    sa.ForeignKeyConstraint(['province_id'], ['province.id'], ),
    sa.ForeignKeyConstraint(['street_id'], ['street.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('feature_district',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('district_id', sa.Integer(), nullable=True),
    sa.Column('feature_id', sa.Integer(), nullable=True),
    sa.Column('value', sa.String(length=64), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['district_id'], ['district.id'], ),
    sa.ForeignKeyConstraint(['feature_id'], ['feature.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('feature_address',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('address_id', sa.Integer(), nullable=True),
    sa.Column('feature_id', sa.Integer(), nullable=True),
    sa.Column('value', sa.String(length=64), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['address_id'], ['address.id'], ),
    sa.ForeignKeyConstraint(['feature_id'], ['feature.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('feature_address')
    op.drop_table('feature_district')
    op.drop_table('address')
    op.drop_index(op.f('ix_street_fias_id'), table_name='street')
    op.drop_table('street')
    op.drop_table('feature_locality')
    op.drop_table('district')
    op.drop_table('locality')
    op.drop_table('feature_area')
    op.drop_table('group_province')
    op.drop_table('feature_province')
    op.drop_table('feature_country')
    op.drop_table('area')
    op.drop_table('province')
    op.drop_table('feature')
    op.drop_table('group')
    op.drop_table('country')
    op.drop_table('category')
    # ### end Alembic commands ###
