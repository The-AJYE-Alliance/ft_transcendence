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