from app import create_app, db
import sqlalchemy as sa

app = create_app()

def upgrade():
    with app.app_context():
        conn = db.engine.connect()
        conn.execute(sa.text("""
            ALTER TABLE books
            ALTER COLUMN title TYPE VARCHAR(500),
            ALTER COLUMN authors TYPE TEXT,
            ALTER COLUMN image_link TYPE TEXT;
        """))
        conn.commit()

if __name__ == '__main__':
    upgrade()
    print("Books table altered successfully.")