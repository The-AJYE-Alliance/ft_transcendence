import {createButton} from "./auth.js";
import {createInput} from "./auth.js";

// Loads a html file at the filePath and returns it as text
export async function loadHTML(filePath) {
    try {
        const response = await fetch(filePath);
        if (!response.ok) {
            throw new Error('Failed to load HTML file');
        }
        return await response.text(); // Return the file content as text
    } catch (error) {
        console.error('Error loading HTML:', error);
        return '<p>Error loading content</p>'; // Return a default error message
    }
}


export function createForm({ action = '', method = 'GET', fields = [], submitText = 'Submit' }) {
    const form = document.createElement('form');
    form.setAttribute('action', action);
    form.setAttribute('method', method);

    fields.forEach(field =>
    {
        if (field.label)
        {
            const label = document.createElement('label');
            label.textContent = field.label;
            label.setAttribute('for', field.name || '');
            form.appendChild(label);
        }
        let input = createInput(field);
        form.appendChild(input);
        form.appendChild(document.createElement('br'));
    });
    const submitButton = createButton(submitText);
    form.appendChild(submitButton);
    return form;
}
