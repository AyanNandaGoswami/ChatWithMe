
function addToList(params) {
    var friend = params;
    var user = JSON.parse(document.getElementById('logged-in-user').textContent);
    let csrfToken = $("input[name=csrfmiddlewaretoken").val();
    $.ajax({
        type: 'POST',
        url: '/account/add-to-list/',
        data: {
            'user': user.username,
            'friend': friend,
            csrfmiddlewaretoken: csrfToken
        },
        dataType: 'json', 
        
        success: function (res) {
            console.log(res);
        }
    });
}
