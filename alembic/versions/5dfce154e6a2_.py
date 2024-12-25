"""empty message

Revision ID: 5dfce154e6a2
Revises: f5970dcd13e9
Create Date: 2024-12-23 15:31:24.585744

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '5dfce154e6a2'
down_revision: Union[str, None] = 'f5970dcd13e9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('temp',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_temp_id'), 'temp', ['id'], unique=False)
    op.drop_index('ix_enrollments_id', table_name='enrollments')
    op.drop_table('enrollments')
    op.drop_index('ix_users_email', table_name='users')
    op.drop_index('ix_users_id', table_name='users')
    op.drop_index('ix_users_telegram_id', table_name='users')
    op.drop_table('users')
    op.drop_index('ix_courses_id', table_name='courses')
    op.drop_table('courses')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('courses',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('courses_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('title', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('description', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='courses_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_index('ix_courses_id', 'courses', ['id'], unique=False)
    op.create_table('users',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('users_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('email', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.Column('telegram_id', sa.BIGINT(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='users_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_index('ix_users_telegram_id', 'users', ['telegram_id'], unique=True)
    op.create_index('ix_users_id', 'users', ['id'], unique=False)
    op.create_index('ix_users_email', 'users', ['email'], unique=True)
    op.create_table('enrollments',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('course_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('enrolled_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['course_id'], ['courses.id'], name='enrollments_course_id_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='enrollments_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='enrollments_pkey'),
    sa.UniqueConstraint('user_id', 'course_id', name='_user_course_uc')
    )
    op.create_index('ix_enrollments_id', 'enrollments', ['id'], unique=False)
    op.drop_index(op.f('ix_temp_id'), table_name='temp')
    op.drop_table('temp')
    # ### end Alembic commands ###
