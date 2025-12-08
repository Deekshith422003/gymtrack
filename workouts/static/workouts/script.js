const API_URL = "/api";

function requireLogin() {
    const token = localStorage.getItem("token");
    if (!token) {
        window.location.href = "index.html";
    }
    return token;
}

// LOGIN
async function login(e) {
    e.preventDefault();
    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value;

    const response = await fetch("/api/token/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password })
    });

    if (!response.ok) {
        alert("Invalid login");
        return;
    }

    const data = await response.json();
    localStorage.setItem("token", data.access);
    window.location.href = "dashboard.html";
}

// LOAD WORKOUTS
async function getWorkouts() {
    const token = requireLogin();

    const response = await fetch(`${API_URL}/workouts/`, {
        headers: { "Authorization": `Bearer ${token}` }
    });

    const workouts = await response.json();
    const table = document.getElementById("workout-list");
    table.innerHTML = "";

    workouts.forEach(w => {
        const entry = w.entries.length ? w.entries[0] : null;
        table.innerHTML += `
            <tr>
                <td>${w.date}</td>
                <td>${entry ? entry.exercise.name : "-"}</td>
                <td>${entry ? entry.sets : "-"}</td>
                <td>${entry ? entry.reps : "-"}</td>
                <td>${w.total_duration} min</td>
                <td>${w.notes || ""}</td>
            </tr>
        `;
    });
}

// SAVE WORKOUT
async function saveWorkout(e) {
    e.preventDefault();
    const token = requireLogin();

    const payload = {
        date: document.getElementById("date").value,
        exercise_name: document.getElementById("exercise").value.trim(),
        sets: parseInt(document.getElementById("sets").value),
        reps: parseInt(document.getElementById("reps").value),
        total_duration: parseInt(document.getElementById("duration").value),
        notes: document.getElementById("notes").value,
    };

    const response = await fetch(`${API_URL}/workouts/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify(payload)
    });

    if (!response.ok) {
        console.error(await response.text());
        alert("Error saving workout");
        return;
    }

    alert("Workout saved!");
    window.location.href = "dashboard.html";
}

function logout() {
    localStorage.removeItem("token");
    window.location.href = "index.html";
}
