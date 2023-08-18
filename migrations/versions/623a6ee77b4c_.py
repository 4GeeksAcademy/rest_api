"""empty message

Revision ID: 623a6ee77b4c
Revises: c2cc58cb4494
Create Date: 2023-08-18 16:03:12.876496

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '623a6ee77b4c'
down_revision = 'c2cc58cb4494'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('favorites',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('planet_id', sa.Integer(), nullable=True),
    sa.Column('people_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['people_id'], ['people.id'], ),
    sa.ForeignKeyConstraint(['planet_id'], ['planet.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('user_favorite_people')
    op.drop_table('user_favorite_planet')
    with op.batch_alter_table('people', schema=None) as batch_op:
        batch_op.alter_column('hair_color',
               existing_type=sa.VARCHAR(length=50),
               type_=sa.String(length=250),
               existing_nullable=False)
        batch_op.alter_column('eye_color',
               existing_type=sa.VARCHAR(length=50),
               type_=sa.String(length=250),
               existing_nullable=False)
        batch_op.alter_column('birth_year',
               existing_type=sa.VARCHAR(length=50),
               type_=sa.String(length=250),
               existing_nullable=False)
        batch_op.drop_column('name')

    with op.batch_alter_table('planet', schema=None) as batch_op:
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(length=50),
               type_=sa.String(length=250),
               existing_nullable=False)
        batch_op.alter_column('climate',
               existing_type=sa.VARCHAR(length=50),
               type_=sa.String(length=250),
               existing_nullable=False)
        batch_op.alter_column('gravity',
               existing_type=sa.VARCHAR(length=50),
               type_=sa.String(length=250),
               existing_nullable=False)
        batch_op.alter_column('terrain',
               existing_type=sa.VARCHAR(length=50),
               type_=sa.String(length=250),
               existing_nullable=False)

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('email',
               existing_type=sa.VARCHAR(length=120),
               type_=sa.String(length=250),
               existing_nullable=False)
        batch_op.alter_column('password',
               existing_type=sa.VARCHAR(length=80),
               type_=sa.String(length=250),
               existing_nullable=False)
        batch_op.drop_constraint('user_email_key', type_='unique')
        batch_op.drop_column('is_active')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_active', sa.BOOLEAN(), autoincrement=False, nullable=False))
        batch_op.create_unique_constraint('user_email_key', ['email'])
        batch_op.alter_column('password',
               existing_type=sa.String(length=250),
               type_=sa.VARCHAR(length=80),
               existing_nullable=False)
        batch_op.alter_column('email',
               existing_type=sa.String(length=250),
               type_=sa.VARCHAR(length=120),
               existing_nullable=False)

    with op.batch_alter_table('planet', schema=None) as batch_op:
        batch_op.alter_column('terrain',
               existing_type=sa.String(length=250),
               type_=sa.VARCHAR(length=50),
               existing_nullable=False)
        batch_op.alter_column('gravity',
               existing_type=sa.String(length=250),
               type_=sa.VARCHAR(length=50),
               existing_nullable=False)
        batch_op.alter_column('climate',
               existing_type=sa.String(length=250),
               type_=sa.VARCHAR(length=50),
               existing_nullable=False)
        batch_op.alter_column('name',
               existing_type=sa.String(length=250),
               type_=sa.VARCHAR(length=50),
               existing_nullable=False)

    with op.batch_alter_table('people', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', sa.VARCHAR(length=50), autoincrement=False, nullable=False))
        batch_op.alter_column('birth_year',
               existing_type=sa.String(length=250),
               type_=sa.VARCHAR(length=50),
               existing_nullable=False)
        batch_op.alter_column('eye_color',
               existing_type=sa.String(length=250),
               type_=sa.VARCHAR(length=50),
               existing_nullable=False)
        batch_op.alter_column('hair_color',
               existing_type=sa.String(length=250),
               type_=sa.VARCHAR(length=50),
               existing_nullable=False)

    op.create_table('user_favorite_planet',
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('planet_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['planet_id'], ['planet.id'], name='user_favorite_planet_planet_id_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='user_favorite_planet_user_id_fkey'),
    sa.PrimaryKeyConstraint('user_id', 'planet_id', name='user_favorite_planet_pkey')
    )
    op.create_table('user_favorite_people',
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('people_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['people_id'], ['people.id'], name='user_favorite_people_people_id_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='user_favorite_people_user_id_fkey'),
    sa.PrimaryKeyConstraint('user_id', 'people_id', name='user_favorite_people_pkey')
    )
    op.drop_table('favorites')
    # ### end Alembic commands ###
