"""empty message

Revision ID: 94bb06877983
Revises: 
Create Date: 2019-08-05 14:12:34.094193

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '94bb06877983'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('first_name', sa.String(length=64), nullable=True),
    sa.Column('last_name', sa.String(length=64), nullable=True),
    sa.Column('location', sa.String(length=128), nullable=True),
    sa.Column('email', sa.String(length=128), nullable=True),
    sa.Column('bio', sa.String(length=1024), nullable=True),
    sa.Column('label', sa.String(length=128), nullable=True),
    sa.Column('portfolio', sa.String(length=1024), nullable=True),
    sa.Column('profile_picture_path', sa.String(length=128), nullable=True),
    sa.Column('discriminator', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_discriminator'), 'user', ['discriminator'], unique=False)
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_first_name'), 'user', ['first_name'], unique=False)
    op.create_index(op.f('ix_user_label'), 'user', ['label'], unique=False)
    op.create_index(op.f('ix_user_last_name'), 'user', ['last_name'], unique=False)
    op.create_index(op.f('ix_user_location'), 'user', ['location'], unique=False)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.create_table('instructor',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('mentor',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('student',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('student_mentor_association',
    sa.Column('student', sa.Integer(), nullable=True),
    sa.Column('mentor', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['mentor'], ['mentor.id'], ),
    sa.ForeignKeyConstraint(['student'], ['student.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('student_mentor_association')
    op.drop_table('student')
    op.drop_table('mentor')
    op.drop_table('instructor')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_location'), table_name='user')
    op.drop_index(op.f('ix_user_last_name'), table_name='user')
    op.drop_index(op.f('ix_user_label'), table_name='user')
    op.drop_index(op.f('ix_user_first_name'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_index(op.f('ix_user_discriminator'), table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###
