"""empty message

Revision ID: 73cd6071ff0b
Revises: 
Create Date: 2019-03-27 20:56:33.842709

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '73cd6071ff0b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('auth',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('url', sa.String(length=255), nullable=True),
    sa.Column('add_time', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name'),
    sa.UniqueConstraint('url')
    )
    op.create_index(op.f('ix_auth_add_time'), 'auth', ['add_time'], unique=False)
    op.create_table('preview',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=True),
    sa.Column('logo', sa.String(length=255), nullable=True),
    sa.Column('add_time', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('title')
    )
    op.create_index(op.f('ix_preview_add_time'), 'preview', ['add_time'], unique=False)
    op.create_table('role',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('auth_list', sa.String(length=255), nullable=True),
    sa.Column('add_time', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_role_add_time'), 'role', ['add_time'], unique=False)
    op.create_table('tag',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('add_time', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_tag_add_time'), 'tag', ['add_time'], unique=False)
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('pwd', sa.String(length=100), nullable=True),
    sa.Column('email', sa.String(length=100), nullable=True),
    sa.Column('phone', sa.String(length=11), nullable=True),
    sa.Column('info', sa.Text(), nullable=True),
    sa.Column('face', sa.String(length=255), nullable=True),
    sa.Column('add_time', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('name'),
    sa.UniqueConstraint('phone')
    )
    op.create_index(op.f('ix_user_add_time'), 'user', ['add_time'], unique=False)
    op.create_table('admin',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('pwd', sa.String(length=100), nullable=True),
    sa.Column('is_super', sa.SmallInteger(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.Column('add_time', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_admin_add_time'), 'admin', ['add_time'], unique=False)
    op.create_table('movie',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=True),
    sa.Column('url', sa.String(length=255), nullable=True),
    sa.Column('info', sa.Text(), nullable=True),
    sa.Column('logo', sa.String(length=255), nullable=True),
    sa.Column('star', sa.SmallInteger(), nullable=True),
    sa.Column('play_num', sa.BigInteger(), nullable=True),
    sa.Column('comment_num', sa.BigInteger(), nullable=True),
    sa.Column('tag_id', sa.Integer(), nullable=True),
    sa.Column('area', sa.String(length=255), nullable=True),
    sa.Column('release_time', sa.Date(), nullable=True),
    sa.Column('length', sa.String(length=100), nullable=True),
    sa.Column('add_time', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['tag_id'], ['tag.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('title')
    )
    op.create_index(op.f('ix_movie_add_time'), 'movie', ['add_time'], unique=False)
    op.create_table('user_log',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('ip', sa.String(length=100), nullable=True),
    sa.Column('add_time', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_log_add_time'), 'user_log', ['add_time'], unique=False)
    op.create_table('admin_log',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('admin_id', sa.Integer(), nullable=True),
    sa.Column('ip', sa.String(length=100), nullable=True),
    sa.Column('add_time', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['admin_id'], ['admin.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_admin_log_add_time'), 'admin_log', ['add_time'], unique=False)
    op.create_table('comment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('movie_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('add_time', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['movie_id'], ['movie.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_comment_add_time'), 'comment', ['add_time'], unique=False)
    op.create_table('movie_col',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('movie_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('add_time', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['movie_id'], ['movie.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_movie_col_add_time'), 'movie_col', ['add_time'], unique=False)
    op.create_table('operation_log',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('admin_id', sa.Integer(), nullable=True),
    sa.Column('ip', sa.String(length=100), nullable=True),
    sa.Column('reason', sa.String(length=600), nullable=True),
    sa.Column('add_time', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['admin_id'], ['admin.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_operation_log_add_time'), 'operation_log', ['add_time'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_operation_log_add_time'), table_name='operation_log')
    op.drop_table('operation_log')
    op.drop_index(op.f('ix_movie_col_add_time'), table_name='movie_col')
    op.drop_table('movie_col')
    op.drop_index(op.f('ix_comment_add_time'), table_name='comment')
    op.drop_table('comment')
    op.drop_index(op.f('ix_admin_log_add_time'), table_name='admin_log')
    op.drop_table('admin_log')
    op.drop_index(op.f('ix_user_log_add_time'), table_name='user_log')
    op.drop_table('user_log')
    op.drop_index(op.f('ix_movie_add_time'), table_name='movie')
    op.drop_table('movie')
    op.drop_index(op.f('ix_admin_add_time'), table_name='admin')
    op.drop_table('admin')
    op.drop_index(op.f('ix_user_add_time'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_tag_add_time'), table_name='tag')
    op.drop_table('tag')
    op.drop_index(op.f('ix_role_add_time'), table_name='role')
    op.drop_table('role')
    op.drop_index(op.f('ix_preview_add_time'), table_name='preview')
    op.drop_table('preview')
    op.drop_index(op.f('ix_auth_add_time'), table_name='auth')
    op.drop_table('auth')
    # ### end Alembic commands ###
