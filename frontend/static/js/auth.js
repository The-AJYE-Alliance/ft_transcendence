import {createForm} from "./utils.js";


export function createAndHandleForm({ app, actionUrl, method, fields, submitText, processData }) {
    const form = createForm({
        action: actionUrl,
        method: method,
        fields: fields,
        submitText: submitText,
    });
    app.innerHTML = '';
    app.appendChild(form);
    form.addEventListener('submit', async (event) => {
        event.preventDefault();
        const formData = new FormData(form);
        let body;
        if (processData)
            body = processData(formData);
        else
            body = formData;
        try {
            const response = await fetch(actionUrl, {
                method: method,
                body: body,
                headers: processData ? { 'Content-Type': 'application/json' } : {},
                credentials: 'include',
            });
            const result = await response.json();
            console.log(`${submitText} successful:`, result);
        } catch (error) {
            console.error(`Error during ${submitText.toLowerCase()}:`, error);
        }
    });
}

export function processLoginData(formData) {
    return JSON.stringify(Object.fromEntries(formData.entries()));
}

