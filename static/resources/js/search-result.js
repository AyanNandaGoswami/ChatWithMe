
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
            if(res['ack'] == 'created') {
                image_id = "friend_request_image_id_" + res['id']
                document.getElementById(image_id).src = 'https://i.postimg.cc/wMm5qvLZ/user-2.png';
            } else if(res['ack'] == 'canceled') {
                image_id = "friend_request_image_id_" + res['id']
                document.getElementById(image_id).src = 'https://i.postimg.cc/J0WFg3q2/add-user.png';
            }
            
        }
    });
}
