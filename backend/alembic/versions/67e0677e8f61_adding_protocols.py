"""adding protocols

Revision ID: 67e0677e8f61
Revises: 6612d313bd94
Create Date: 2024-05-19 12:26:13.506937

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision: str = '67e0677e8f61'
down_revision: Union[str, None] = '6612d313bd94'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    PROTOCOLS = [
        ('vless', 'vless'),
        ('trojan', 'trojan')
    ]
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('inbounds', sa.Column('protocol', sqlalchemy_utils.types.choice.ChoiceType(PROTOCOLS)))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('inbounds', 'protocol')
    # ### end Alembic commands ###
