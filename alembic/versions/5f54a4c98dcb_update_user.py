"""update user

Revision ID: 5f54a4c98dcb
Revises: f27225b0f401
Create Date: 2024-12-19 01:59:33.903971

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5f54a4c98dcb'
down_revision: Union[str, None] = 'f27225b0f401'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('_user_course_uc', 'enrollments', ['user_id', 'course_id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('_user_course_uc', 'enrollments', type_='unique')
    # ### end Alembic commands ###
