import sqlalchemy as sa
from app.db import metadata

event_categories_table = sa.Table(
    'event_categories',
    metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('title', sa.String)
)

events_table = sa.Table(
    'events',
    metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('title', sa.String, nullable=False),
    sa.Column('date', sa.String, nullable=True),
    sa.Column('short_description', sa.String, nullable=True),
    sa.Column('description', sa.String, nullable=True),
    sa.Column('place', sa.String, nullable=True),
    sa.Column('image_url', sa.String, nullable=True),
    sa.Column('category_id', sa.Integer, sa.ForeignKey('event_categories.id'))
)
