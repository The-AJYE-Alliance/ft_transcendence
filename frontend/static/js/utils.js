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
        if (field.autocomplete)
            input.setAttribute('autocomplete', field.autocomplete);
        else
            input.setAttribute('autocomplete', 'on');
        if (field.value)
            input.value = field.value;
        if (field.label)
        {
            const label = document.createElement('label');
            label.textContent = field.label;
            label.setAttribute('for', fieldId);
            form.appendChild(label);
        }
        form.appendChild(input);
        form.appendChild(document.createElement('br'));
    });
    const submitButton = document.createElement('button');
    submitButton.setAttribute('type', 'submit');
    submitButton.textContent = submitText;
    form.appendChild(submitButton);
    return form;
}
