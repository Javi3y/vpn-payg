"""adding clients

Revision ID: bbe16ac2f7d7
Revises: 67e0677e8f61
Create Date: 2024-05-20 11:13:02.529386

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision: str = 'bbe16ac2f7d7'
down_revision: Union[str, None] = '67e0677e8f61'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('clients',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uuid', sqlalchemy_utils.types.uuid.UUIDType(), server_default=sa.text('uuid_generate_v4()'), nullable=False),
    sa.Column('usage', sa.Integer(), server_default='0', nullable=True),
    sa.Column('user', sa.Integer(), nullable=False),
    sa.Column('inbound', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['inbound'], ['inbounds.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('clients')
    # ### end Alembic commands ###