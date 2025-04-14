// Main JavaScript for Startup Onboarding Platform

// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Add confirmation for status change buttons
    setupStatusChangeConfirmation();
    
    // Setup form validation
    setupFormValidation();
});

/**
 * Add confirmation dialogs for status change buttons
 */
function setupStatusChangeConfirmation() {
    // Get all status change buttons
    const acceptButtons = document.querySelectorAll('.btn-accept');
    const rejectButtons = document.querySelectorAll('.btn-reject');
    const resetButtons = document.querySelectorAll('.btn-reset');
    
    // Add confirmation for accept buttons
    acceptButtons.forEach(button => {
        if (!button.disabled) {
            button.addEventListener('click', function(e) {
                if (!confirm('Are you sure you want to ACCEPT this startup?')) {
                    e.preventDefault();
                }
            });
        }
    });
    
    // Add confirmation for reject buttons
    rejectButtons.forEach(button => {
        if (!button.disabled) {
            button.addEventListener('click', function(e) {
                if (!confirm('Are you sure you want to REJECT this startup?')) {
                    e.preventDefault();
                }
            });
        }
    });
    
    // Add confirmation for reset buttons
    resetButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to reset the status of this startup to PENDING?')) {
                e.preventDefault();
            }
        });
    });
}

/**
 * Setup form validation for create startup form
 */
function setupFormValidation() {
    const form = document.querySelector('.startup-form');
    
    if (form) {
        form.addEventListener('submit', function(e) {
            const nameField = document.getElementById('name');
            let isValid = true;
            
            // Name validation (required)
            if (!nameField.value.trim()) {
                highlightError(nameField, 'Startup name is required');
                isValid = false;
            } else {
                removeError(nameField);
            }
            
            // Year validation (if provided)
            const yearField = document.getElementById('founded_year');
            if (yearField.value) {
                const year = parseInt(yearField.value);
                const currentYear = new Date().getFullYear();
                
                if (isNaN(year) || year < 1900 || year > currentYear) {
                    highlightError(yearField, `Year must be between 1900 and ${currentYear}`);
                    isValid = false;
                } else {
                    removeError(yearField);
                }
            }
            
            // Website validation (if provided)
            const websiteField = document.getElementById('website');
            if (websiteField.value && !isValidURL(websiteField.value)) {
                highlightError(websiteField, 'Please enter a valid URL (e.g., https://example.com)');
                isValid = false;
            } else {
                removeError(websiteField);
            }
            
            if (!isValid) {
                e.preventDefault();
            }
        });
    }
}

/**
 * Highlight form field with error
 */
function highlightError(field, message) {
    // Remove any existing error
    removeError(field);
    
    // Add error class to field
    field.classList.add('error-field');
    
    // Create error message element
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.innerText = message;
    
    // Insert error message after the field
    field.parentNode.insertBefore(errorDiv, field.nextSibling);
}

/**
 * Remove error highlighting from field
 */
function removeError(field) {
    field.classList.remove('error-field');
    
    // Remove any existing error message
    const nextElement = field.nextElementSibling;
    if (nextElement && nextElement.className === 'error-message') {
        nextElement.remove();
    }
}

/**
 * Validate URL format
 */
function isValidURL(url) {
    try {
        new URL(url);
        return true;
    } catch {
        return false;
    }
}

// Add styles for form validation
const style = document.createElement('style');
style.textContent = `
    .error-field {
        border-color: var(--danger-color) !important;
    }
    
    .error-message {
        color: var(--danger-color);
        font-size: 0.8rem;
        margin-top: 5px;
    }
`;
document.head.appendChild(style);