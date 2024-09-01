from app import create_app, db
import sqlalchemy as sa

app = create_app()

def upgrade():
    with app.app_context():
        conn = db.engine.connect()
        
        # Alter books table
        conn.execute(sa.text("""
            ALTER TABLE books
            ALTER COLUMN title TYPE VARCHAR(500),
            ALTER COLUMN authors TYPE TEXT,
            ALTER COLUMN image_link TYPE TEXT;
        """))
        
        # Alter users table (if needed)
        conn.execute(sa.text("""
            ALTER TABLE users
            ALTER COLUMN username TYPE VARCHAR(64),
            ALTER COLUMN email TYPE VARCHAR(120);
        """))
        
        # Alter cart_items table (if needed)
        conn.execute(sa.text("""
            ALTER TABLE cart_items
            ALTER COLUMN quantity SET DEFAULT 1;
        """))
        
        conn.commit()

if __name__ == '__main__':
    upgrade()
    print("Tables altered successfully.")