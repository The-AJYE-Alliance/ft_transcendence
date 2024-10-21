import {loadHTML} from './utils.js'
import { createForm } from './utils.js';
import Router from './router.js'

const app = document.getElementById('app');
const router = new Router(app);
//const router = new Router()
// Dynamic content will be generated inside the app <div>, everything before will stay static
//const app = document.getElementById('app')

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

router.get('/register', () => {
    const myForm = createForm({
        action: '/submit-form',
        method: 'POST',
        fields: [
            { type: 'text', name: 'username', placeholder: 'Enter your username', label: 'Username:' },
            { type: 'password', name: 'password', placeholder: 'Enter your password', label: 'Password:' },
            { type: 'email', name: 'email', placeholder: 'Enter your email', label: 'Email:' }
        ],
        submitText: 'Sign Up'
    });

    // Nettoie l'élément app et ajoute le formulaire
    app.innerHTML = '';
    app.appendChild(myForm);

    // Ajoute un gestionnaire pour la soumission du formulaire
    myForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        const formData = new FormData(myForm);
        const data = Object.fromEntries(formData.entries());

        try {
            const response = await fetch('/submit-form', {
                method: 'POST',
                body: JSON.stringify(data),
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            const result = await response.json();
            console.log('Form submission successful:', result);
        } catch (error) {
            console.error('Error during form submission:', error);
        }
    });
});

