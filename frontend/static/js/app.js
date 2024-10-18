
const homepage = document.getElementById('homepage');
const loginPage = document.getElementById('login-page');
const registerPage = document.getElementById('register-page');


const goToLoginBtn = document.getElementById('go-to-login');
const goToRegisterBtn = document.getElementById('go-to-register');

goToLoginBtn.addEventListener('click', () => {
    homepage.style.display = 'none';
    loginPage.style.display = 'block';
});

goToRegisterBtn.addEventListener('click', () => {
    homepage.style.display = 'none';
    registerPage.style.display = 'block';
});


document.getElementById('form-login').addEventListener('submit', async (e) => {
    e.preventDefault();

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    const response = await fetch('/login/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
    });

    if (response.ok) {
        const data = await response.json();
        alert('Login successful!');
    } else {
        alert('Login failed');
    }
});


document.getElementById('form-register').addEventListener('submit', async (e) => {
    e.preventDefault();

    const username = document.getElementById('username-register').value;
    const email = document.getElementById('email-register').value;
    const password = document.getElementById('password-register').value;
    const nickname = document.getElementById('nickname-register').value;

    const response = await fetch('/register/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, email, password, nickname })
    });

    if (response.ok) {
        alert('Registration successful!');
    } else {
        alert('Registration failed');
    }
});
