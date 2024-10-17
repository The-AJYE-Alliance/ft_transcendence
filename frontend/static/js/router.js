class Router {
    constructor() {
        this.get('/', () => {})
        this.get('/404', () => {})

        document.addEventListener('click', (event) => {
            const target = event.target.closest('a')

            if (!target) {
                return
            }

            const url = target.getAttribute('href')
            if (this.#startsWithHash(url)) {
                return
            }

            if (target.hostname === location.hostname) {
                event.preventDefault()
                this.#redirect(url)
            }
        }, false)

        window.addEventListener('DOMContentLoaded', (event) => {
            event.preventDefault()
            this.#checkPatterns(location.pathname + location.hash)
        })

        window.addEventListener('popstate', () => {
            this.#checkPatterns(location.pathname + location.hash)
        })
    }

    #paths = {}
    #previousPath = null

    #redirect(url) {
        if (url === '/404') {
            window.history.replaceState(null, null, url)
        } else {
            window.history.pushState(null, null, url)
        }
        this.#checkPatterns(url)
    }

    #handleError() {
        console.error('Page not found')
        this.#redirect('/404')
    }

    #transformRegexOutput(input) {
        try {
            return Object
                .keys(input)
                .filter(key => Number(key))
                .reduce((obj, key) => { return { ...obj, [key]: input[key] } }, {})
        } catch (error) {
            this.#handleError()
            return {}
        }
    }

    #mergeObjects(obj1, obj2) {
        let iterator = -1
        return Object
            .entries(obj1)
            .reduce((obj, key, index) => {
                if (obj1[index + 1] === '*') { iterator += 1 }
                return ({ ...obj, [obj1[index + 1] === '*' ? iterator : obj1[index + 1].substring(1)]: obj2[index + 1] })
            }, {})
    }

    #parsePatterns(pattern) {
        return `^${pattern
            .replace(/\\/g, '\\/')
            .replace(/(\*|:\w*)/gm, '(:?[A-z0-9|*]*)')}(?:\\/?)$`
    }

    get(pattern, callback) {
        const paths = this.#paths

        if (!paths[pattern]) {
            paths[pattern] = {}
            paths[pattern].callbacks = []
        }

        paths[pattern].reg = this.#parsePatterns(pattern)
        paths[pattern].callbacks.push(callback)
        return true
    }

    #checkIfAnyPatternIsMatching(url) {
        return (element) => {
            const pattern = this.#paths[element].reg
            const newRegex = new RegExp(pattern, 'i').exec(url)
            if (!newRegex) { return false }
            return true
        }
    }

    #startsWithHash(string) {
        const regEx = /^#/
        const startsWithHash = regEx.test(string)
        return Boolean(startsWithHash)
    }
}