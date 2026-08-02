from app import create_app
from app.seed import seed_data


def run_smoke_test():
    app = create_app()
    # Seed data using the app context (this will create a local SQLite DB by default)
    seed_data()

    client = app.test_client()

    resp = client.get('/courses')
    print('GET /courses status code:', resp.status_code)
    if resp.status_code != 200:
        print('Response data:', resp.get_data(as_text=True))
        raise SystemExit('Smoke test failed: /courses returned non-200')

    data = resp.get_json()
    courses = data.get('courses') if data else None
    print('Courses returned:', len(courses) if courses is not None else 'no data')

    assert resp.status_code == 200
    assert courses is not None and len(courses) > 0


if __name__ == '__main__':
    run_smoke_test()
