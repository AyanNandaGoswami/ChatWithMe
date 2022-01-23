
function addToList(params) {
    var friend = params;
    var user = JSON.parse(document.getElementById('logged-in-user').textContent);
    let csrfToken = $("input[name=csrfmiddlewaretoken").val();
    $.ajax({
        type: 'POST',
        url: '/account/send-friend-request/',
        data: {
            'user': user.username,
            'friend': friend,
            csrfmiddlewaretoken: csrfToken
        },
        dataType: 'json', 
        
        success: function (res) {
            document.getElementById('friend_request_image_id').src = 'https://i.postimg.cc/wMm5qvLZ/user-2.png';
            alert("Friend request send to " + friend);
        }
    });
}
