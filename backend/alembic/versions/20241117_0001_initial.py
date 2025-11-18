from __future__ import annotations
from alembic import op
import sqlalchemy as sa
from pgvector.sqlalchemy import Vector

revision = '20241117_0001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.execute("CREATE EXTENSION IF NOT EXISTS vector;")
    op.create_table(
        'documents',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('doc_type', sa.String(50), index=True),
        sa.Column('title', sa.String(255)),
        sa.Column('content', sa.Text),
        sa.Column('metadata', sa.JSON),
        sa.Column('embedding', Vector(1536)),
    )
    op.create_table(
        'tenders',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('document_id', sa.Integer, sa.ForeignKey('documents.id'), nullable=False),
        sa.Column('summary', sa.Text),
        sa.Column('boq', sa.JSON),
        sa.Column('risks', sa.JSON),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP')),
    )
    op.create_table(
        'chat_messages',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('session_id', sa.String(64), index=True),
        sa.Column('role', sa.String(16)),
        sa.Column('content', sa.Text),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP')),
    )
    op.create_table(
        'feedback',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('chat_message_id', sa.Integer, sa.ForeignKey('chat_messages.id')),
        sa.Column('correction', sa.Text),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP')),
    )
    op.create_table(
        'memory',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('key', sa.String(128), index=True),
        sa.Column('value', sa.Text),
        sa.Column('metadata', sa.JSON),
        sa.Column('embedding', Vector(1536)),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP')),
    )


def downgrade():
    op.drop_table('memory')
    op.drop_table('feedback')
    op.drop_table('chat_messages')
    op.drop_table('tenders')
    op.drop_table('documents')
