from sqlalchemy import create_engine, text
engine = create_engine('postgresql://postgres:postgres@localhost:5432/hotel_management')
with engine.connect() as conn:
    result = conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema='public'"))
    tables = result.fetchall()
    print('Tables created:')
    for t in tables:
        print(f'  - {t[0]}')