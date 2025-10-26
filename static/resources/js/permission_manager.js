function showSection(sectionId) {
  const sections = ['endpoints', 'permissions', 'users'];
  sections.forEach(id => {
    document.getElementById(id).classList.remove('active');
  });
  document.getElementById(sectionId).classList.add('active');
}

document.addEventListener('DOMContentLoaded', function () {
  loadEndpoints();
});

function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}

function loadEndpoints() {
  const token = getCookie("authToken");
  if (!token) {
    alert('Authorization token is missing.');
    return;
  }

  $.ajax({
    type: 'GET',
    url: 'http://localhost:8080/permission/v1/endpoint/all',
    headers: {
      'Authorization': 'Bearer ' + token
    },
    contentType: 'application/json',
    dataType: 'json',
    success: function (data) {
      const $list = $('#endpointList');
      $list.empty();

      if (data.length === 0) {
        $list.append('<li class="list-group-item">No endpoints found.</li>');
      } else {
        data.forEach(endpoint => {
          $list.append(`
            <li class="list-group-item d-flex justify-content-between align-items-center">
              <div>
                <strong>${endpoint.name}</strong><br>
                <small>${endpoint.method} ${endpoint.url}</small>
              </div>
              <span>
                <button class="btn btn-sm btn-warning">Edit</button>
                <button class="btn btn-sm btn-danger">Delete</button>
              </span>
            </li>
          `);
        });
      }
    },
    error: function (xhr) {
      if (
        xhr.status === 401 &&
        xhr.responseJSON &&
        xhr.responseJSON.message === " token is expired"
      ) {
        window.location.href = "/login";
      } else if  (
        xhr.status === 403
      ) {
        showPermissionDenied();
      } else {
        console.error(xhr);
      }
    }
  });
}

function submitEndpoint() {
  const name = $('#name').val().trim();
  const url = $('#url').val().trim();
  const method = $('#endpointMethod').val();
  const token = getCookie("authToken");
  if (!token) {
    alert('Authorization token is missing.');
    return;
  }

  if (!name || !url || !method) {
    alert('Please fill all fields.');
    return;
  }

  $.ajax({
    url: 'http://localhost:8080/permission/v1/endpoint/add/',
    method: 'POST',
    contentType: 'application/json',
    headers: {
      'Authorization': 'Bearer ' + token
    },
    data: JSON.stringify({
      name: name,
      url: url,
      method: method
    }),
    success: function () {
      alert('Endpoint added successfully');
      $('#addEndpointModal').modal('hide');
      $('#endpointForm')[0].reset();
      loadEndpoints(); // Reload updated list
    },
    error: function (xhr) {
        console.log(xhr)
      const response = xhr.responseJSON;
      if (
        xhr.status === 401 &&
        response &&
        response.message === " token is expired"
      ) {
        window.location.href = "/login";
        return;
      } else if  (
        xhr.status === 403
      ) {a
        showPermissionDenied();
        return
      }

      const errorContainer = document.getElementById('error-msg');
      errorContainer.innerHTML = '';

      const fieldIds = ['name', 'url'];
      fieldIds.forEach(id => {
        const input = document.getElementById(id);
        const errorDiv = document.getElementById(id + '_err_id');
        if (input) input.classList.remove('is-invalid');
        if (errorDiv) errorDiv.innerHTML = '';
      });

      if (Array.isArray(response)) {
        // Field-level validation errors
        response.forEach(err => {
          const field = err.field_name.toLowerCase();
          const message = err.message;

          const input = document.getElementById(field);
          const errorDiv = document.getElementById(field + '_err_id');

          if (input) input.classList.add('is-invalid');
          if (errorDiv) errorDiv.innerHTML = message;
        });
      } else if (response && response.message) {
        errorContainer.innerHTML = response.message;
      } else {
        errorContainer.innerHTML = "An error occurred. Please try again.";
      }
    }
  });
}
