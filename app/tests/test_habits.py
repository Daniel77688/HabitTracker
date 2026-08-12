def test_create_habit(client, registered_user):
    user_id = registered_user["id"]
    response = client.post(
        "/habits/",
        json={"title": "Hacer Ejercicio", "description": "30 mins al día", "frequency_type": "daily", "user_id": user_id}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Hacer Ejercicio"
    assert data["id"] is not None

def test_create_habit_requires_user_id(client):
    response = client.post(
        "/habits/",
        json={"title": "Hábito sin user_id", "frequency_type": "daily"}
    )
    assert response.status_code == 400

def test_get_habits_by_user(client, registered_user):
    user_id = registered_user["id"]
    client.post("/habits/", json={"title": "Leer 20 mins", "frequency_type": "daily", "user_id": user_id})
    response = client.get(f"/habits/user/{user_id}")
    assert response.status_code == 200
    assert len(response.json()) >= 1
    assert response.json()[0]["title"] == "Leer 20 mins"

def test_update_habit(client, registered_user):
    user_id = registered_user["id"]
    habit_res = client.post(
        "/habits/",
        json={"title": "Meditar", "frequency_type": "daily", "user_id": user_id}
    )
    habit_id = habit_res.json()["id"]

    update_res = client.put(f"/habits/{habit_id}", json={"title": "Meditar 10 mins"})
    assert update_res.status_code == 200
    assert update_res.json()["title"] == "Meditar 10 mins"

def test_delete_habit(client, registered_user):
    user_id = registered_user["id"]
    habit_res = client.post(
        "/habits/",
        json={"title": "Hábito a eliminar", "frequency_type": "daily", "user_id": user_id}
    )
    habit_id = habit_res.json()["id"]

    delete_res = client.delete(f"/habits/{habit_id}")
    assert delete_res.status_code == 200
    assert delete_res.json()["message"] == "Habit deleted successfully"
