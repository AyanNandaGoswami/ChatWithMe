window.onload = initAll;

var login_btn;

function initAll() {
    document.getElementById('login-btn').addEventListener('click', login);
}

function login() {
    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;

    let csrfToken = $("input[name=csrfmiddlewaretoken").val();

    if(fields_are_not_null() == false) {
        return false;
    }

    $.ajax({
        type: 'POST',
        url: '/account/user-login/',
        data: {
            'username': username,
            'password': password,
            csrfmiddlewaretoken: csrfToken
        },
        dataType: 'json', 
        
        success: function (res, status) {
            if(res.is_authenticated==true){
                var url = '/profile';
                document.location.href = url;
            } else {
                // cleanForm();
                document.getElementById('username').classList.add('is-invalid');
                document.getElementById('password').classList.add('is-invalid');
                document.getElementById('error-msg').innerHTML = 'Invalid login credentials.';
                setTimeout(function() {
                    document.getElementById('error-msg').innerHTML = '';    
                }, 3000);
            }
        }
    });
    
}


function fields_are_not_null() {    
    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;

    if(username == '') {
        document.getElementById('username').classList.add('is-invalid');
        document.getElementById('username_err_id').innerHTML="This field is required.";
        return false;
    }
    document.getElementById('username').classList.remove('is-invalid');
    document.getElementById('username_err_id').innerHTML="";

    if(password == '') {
        document.getElementById('password').classList.add('is-invalid');
        document.getElementById('password_err_id').innerHTML="This field is required.";
        return false;   
    }
    document.getElementById('password').classList.remove('is-invalid');
    document.getElementById('password_err_id').innerHTML="";
}

function cleanForm() {
    document.getElementById('username').value = '';
    document.getElementById('password').value = '';
}

