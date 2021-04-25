window.onload = initAll;

function initAll() {
    document.getElementById('reg-btn').addEventListener('click', register);
}

function register() {
    var fullname = document.getElementById('fullname').value;
    var email = document.getElementById('email').value;
    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;

    let csrfToken = $("input[name=csrfmiddlewaretoken").val();
    $.ajax({
        type: 'POST',
        url: '/account/create-new-user/',
        data: {
            'first_name': fullname,
            'email': email,
            'username': username,
            'password': password,
            csrfmiddlewaretoken: csrfToken
        },
        dataType: 'json', 
        
        success: function (res) {
            var login_status = false;
            login_status = res['login'];
            if(login_status == true) {
                var url = '/profile';
                document.location.href = url;
            } else {
                document.getElementById('error-msg').innerHTML = res['username'];
            }
        }
    }); 
}


