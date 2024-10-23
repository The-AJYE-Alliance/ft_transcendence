import {createForm} from "./utils.js";


export function createButton(submitText) {
    const submitButton = document.createElement('button');
    submitButton.setAttribute('type', 'submit');
    submitButton.textContent = submitText;
    return submitButton;
}

export function createInput(field)
{
    let input;
        const fieldId = field.name || '';
        if (field.type === 'textarea')
            input = document.createElement('textarea');
        else if (field.type === 'select')
        {
            input = document.createElement('select');
            field.options.forEach(optionData => {
                const option = document.createElement('option');
                option.value = optionData.value;
                option.textContent = optionData.text;
                input.appendChild(option);
            });
        }
        else
        {
            input = document.createElement('input');
            input.setAttribute('type', field.type || 'text');
        }
        input.setAttribute('id', fieldId);
        input.setAttribute('name', field.name || '');
        input.setAttribute('placeholder', field.placeholder || '');
        input.setAttribute('autocomplete', field.autocomplete || 'on')
        if (field.value)
            input.value = field.value;
        return input;
}

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

