"""empty message

Revision ID: e78b0e7d8206
Revises: c63cd07ec4c3
Create Date: 2024-06-17 18:48:06.860637

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e78b0e7d8206'
down_revision: Union[str, None] = 'c63cd07ec4c3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('values', sa.Column('core_value', sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('values', 'core_value')
    # ### end Alembic commands ###