// ===============================
// CONFIGURACIÓN
// ===============================
const API_URL = "https://sistema-predictivo-pymes.onrender.com";

// ===============================
// TOKEN
// ===============================
function getToken() {
    return localStorage.getItem("token");
}

function checkAuth() {
    if (!getToken()) {
        window.location.href = "../pages/login.html";
    }
}

// ===============================
// LOGIN
// ===============================
const loginForm = document.getElementById("loginForm");

if (loginForm) {
    loginForm.addEventListener("submit", async (e) => {
        e.preventDefault();

        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;

        const res = await fetch(`${API_URL}/auth/login`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password })
        });

        if (!res.ok) {
            document.getElementById("error").innerText = "Credenciales incorrectas ❌";
            return;
        }

        const data = await res.json();
        localStorage.setItem("token", data.access_token);

        window.location.href = "../pages/dashboard.html";
    });
}

// ===============================
// LOGOUT
// ===============================
function logout() {
    localStorage.removeItem("token");
    window.location.href = "../pages/login.html";
}
