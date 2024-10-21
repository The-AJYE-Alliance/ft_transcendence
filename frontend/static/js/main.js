import {loadHTML} from './utils.js'
import Router from './router.js'

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