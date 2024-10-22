import {loadHTML} from './utils.js'
import { createForm } from './utils.js';
import Router from './router.js'
import { createAndHandleForm, processLoginData } from './auth.js';


const router = new Router()
// Dynamic content will be generated inside the app <div>, everything before will stay static
const app = document.getElementById('app')


// Here we are generating our routes, using callback that are doing basic things for the moment.
// The callbacks will become bigger functions that are generating dynamic content for every services.
router.get('/', async () => {
    app.innerHTML = await loadHTML('../home.html')
})

router.get('/bonjour', async () => {
    app.innerHTML = await loadHTML('../bonjour.html')
})

router.get('/404', () => {
  app.innerHTML = '<p style="text-align: center">404 Not found</p>';
});

router.get('/login', () => {
    createAndHandleForm({
        app: app,
        actionUrl: 'https://auth.api.transcendence.local/login/',
        method: 'POST',
        fields: [
            { type: 'text', name: 'username', placeholder: 'Enter your username', label: 'Username:' },
            { type: 'password', name: 'password', placeholder: 'Enter your password', label: 'Password:' }
        ],
        submitText: 'Log In',
        processData: processLoginData,
    });
});

router.get('/login/42', () => {
    const oauthButton = document.createElement('button');
    oauthButton.textContent = 'Log in with 42';
    oauthButton.addEventListener('click', () => {
        window.location.href = 'https://auth.api.transcendence.local/login/42/';
    });
    app.innerHTML = '';
    app.appendChild(oauthButton);
});


router.get('/register', () => {
    createAndHandleForm({
        app: app,
        actionUrl: 'https://auth.api.transcendence.local/register/',
        method: 'POST',
        fields: [
            { type: 'text', name: 'username', placeholder: 'Enter your username', label: 'Username:'},
            { type: 'email', name: 'email', placeholder: 'Enter your email', label: 'Email:' },
            { type: 'password', name: 'password', placeholder: 'Enter your password', label: 'Password:' },
            { type: 'text', name: 'nickname', placeholder: 'Enter your nickname', label: 'Nickname:' },
            { type: 'file', name: 'avatar', label: 'Avatar:' },
        ],
        submitText: 'Register',
    });
});

