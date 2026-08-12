def test_daily_streak_increment(client, registered_user):
    user_id = registered_user["id"]
    habit_res = client.post(
        "/habits/",
        json={"title": "Agua 2L", "frequency_type": "daily", "user_id": user_id}
    )
    assert habit_res.status_code == 201
    habit_id = habit_res.json()["id"]

    log_res = client.post("/habit-logs/", json={"habit_id": habit_id, "notes": "Completado"})
    assert log_res.status_code == 201

    streak_res = client.get(f"/streaks/habit/{habit_id}")
    assert streak_res.status_code == 200
    assert streak_res.json()["current_streak"] == 1
    assert streak_res.json()["longest_streak"] == 1

def test_weekly_streak_increment(client, registered_user):
    user_id = registered_user["id"]
    habit_res = client.post(
        "/habits/",
        json={"title": "Lavar Coche", "frequency_type": "weekly", "user_id": user_id}
    )
    assert habit_res.status_code == 201
    habit_id = habit_res.json()["id"]

    log_res = client.post("/habit-logs/", json={"habit_id": habit_id})
    assert log_res.status_code == 201

    streak_res = client.get(f"/streaks/habit/{habit_id}")
    assert streak_res.status_code == 200
    assert streak_res.json()["current_streak"] == 1

def test_monthly_streak_increment(client, registered_user):
    user_id = registered_user["id"]
    habit_res = client.post(
        "/habits/",
        json={"title": "Revisar Presupuesto", "frequency_type": "monthly", "user_id": user_id}
    )
    assert habit_res.status_code == 201
    habit_id = habit_res.json()["id"]

    client.post("/habit-logs/", json={"habit_id": habit_id})

    streak_res = client.get(f"/streaks/habit/{habit_id}")
    assert streak_res.status_code == 200
    assert streak_res.json()["current_streak"] == 1

def test_custom_streak_increment(client, registered_user):
    user_id = registered_user["id"]
    habit_res = client.post(
        "/habits/",
        json={"title": "Gimnasio L-M-V", "frequency_type": "custom", "target_days": [0, 2, 4], "user_id": user_id}
    )
    assert habit_res.status_code == 201
    habit_id = habit_res.json()["id"]

    client.post("/habit-logs/", json={"habit_id": habit_id})

    streak_res = client.get(f"/streaks/habit/{habit_id}")
    assert streak_res.status_code == 200
    assert streak_res.json()["current_streak"] == 1
