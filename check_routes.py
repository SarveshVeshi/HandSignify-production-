from app import app
with app.app_context():
    print("--- URL MAP ---")
    for rule in app.url_map.iter_rules():
        print(f"{rule.rule} -> {rule.endpoint}")
