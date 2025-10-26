window.onload = initAll;

function initAll() {
    document.getElementById('reg-btn').addEventListener('click', register);
}

function register() {
    const firstname = document.getElementById('firstname').value.trim();
    const middlename = document.getElementById('middlename').value.trim();
    const lastname = document.getElementById('lastname').value.trim();
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value.trim();
    const isadmin = document.getElementById('isadmin').checked;

    const csrfToken = $("input[name=csrfmiddlewaretoken]").val();

    if (!fields_are_not_null()) {
        return false;
    }

    $.ajax({
        type: 'POST',
        url: 'http://localhost:4001/auth/v1/register/',
        data: JSON.stringify({
            firstname: firstname,
            middlename: middlename,
            lastname: lastname,
            email: email,
            password: password,
            isadmin: isadmin
        }),
        contentType: 'application/json',
        dataType: 'json',
        success: function (res, status, xhr) {
            if (xhr.status === 200 && res.message === "Account created successfully.") {
                window.location.href = "/login";
            } else {
                document.getElementById('error-msg').innerHTML = res.message || "Registration failed.";
            }
        },
        error: function (xhr) {
            const errorContainer = document.getElementById('error-msg');
            errorContainer.innerHTML = '';

            // Clear previous field errors
            const fieldIds = ['firstname', 'middlename', 'lastname', 'email', 'password'];
            fieldIds.forEach(id => {
                const input = document.getElementById(id);
                const errorDiv = document.getElementById(id + '_err_id');
                if (input) input.classList.remove('is-invalid');
                if (errorDiv) errorDiv.innerHTML = '';
            });
            const response = xhr.responseJSON;

            if (Array.isArray(response)) {
                // Field-level errors
                response.forEach(err => {
                    const field = err.field_name.toLowerCase();
                    const message = err.message;

                    const input = document.getElementById(field);
                    const errorDiv = document.getElementById(field + '_err_id');

                    if (input) input.classList.add('is-invalid');
                    if (errorDiv) errorDiv.innerHTML = message;
                });
            } else if (response && response.message) {
                // General error message
                errorContainer.innerHTML = response.message;
            } else {
                // Fallback
                errorContainer.innerHTML = "An error occurred. Please try again.";
            }
        }
    });
}

function fields_are_not_null() {
    let hasError = false;

    const fields = [
        { id: 'firstname', required: true },
        { id: 'lastname', required: true },
        { id: 'email', required: true },
        { id: 'password', required: true }
    ];

    fields.forEach(field => {
        const input = document.getElementById(field.id);
        const errorDiv = document.getElementById(field.id + '_err_id');

        if (field.required && input.value.trim() === '') {
            input.classList.add('is-invalid');
            if (errorDiv) errorDiv.innerHTML = "This field is required.";
            hasError = true;
        } else {
            input.classList.remove('is-invalid');
            if (errorDiv) errorDiv.innerHTML = "";
        }
    });

    return !hasError;
}

function cleanForm() {
    const inputsToClear = ['firstname', 'middlename', 'lastname', 'email', 'password'];
    inputsToClear.forEach(id => {
        const input = document.getElementById(id);
        if (input) input.value = '';
    });

    const isAdmin = document.getElementById('isadmin');
    if (isAdmin) isAdmin.checked = false;

    document.getElementById('error-msg').innerHTML = '';
}
