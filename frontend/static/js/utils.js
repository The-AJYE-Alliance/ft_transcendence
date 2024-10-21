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
    form.action = action;
    form.method = method;

    fields.forEach(field => {
        const input = document.createElement('input');
        input.type = field.type || 'text';
        input.name = field.name || '';
        input.placeholder = field.placeholder || '';
        if (field.value)
            input.value = field.value;
        if (field.label) {
            const label = document.createElement('label');
            label.textContent = field.label;
            label.setAttribute('for', field.name);
            form.appendChild(label);
        }

        form.appendChild(input);
        form.appendChild(document.createElement('br'));
    });

    const submitButton = document.createElement('button');
    submitButton.type = 'submit';
    submitButton.textContent = submitText;
    form.appendChild(submitButton);

    return form;
}