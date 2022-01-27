
function unfriend(params) {
    var friend = params;
    var user = JSON.parse(document.getElementById('logged-in-user').textContent);
    let csrfToken = $("input[name=csrfmiddlewaretoken").val();
    $.ajax({
        type: 'POST',
        url: '/account/unfriend/',
        data: {
            'user': user.id,
            'friend': friend,
            csrfmiddlewaretoken: csrfToken
        },
        dataType: 'json', 
        
        success: function (res) {
            console.log(res);
            
            if(res.length === 0) {
                var list_container = document.querySelector('#list-container-id');
                list_container.innerHTML = "<p id=\"no-contacts\">No contacts yet.</p>";
            } else {
                var list_container = document.querySelector('#list-container-id');
                var temp = res.map(item=>(
                    "<div class=\"row my-row\"><div class=\"col-md-2 my-col\"><a href=\"/chatroom/" + item.username + "/\" class=\"my-anchor\"><img src=\"https://bootdey.com/img/Content/avatar/avatar1.png\" class=\"profile-image\"></a></div><div class=\"col-md-5 my-col\">  <a href=\"/chatroom/" + item.username + "/\" class=\"my-anchor\"><p class=\"profile-name\">" + item.first_name + "</p><p class=\"last-messsage\">"+ item.me + item.last_message +"</p></a></div><div class=\"col-md-3 my-col\"><p class=\"datetime\">"+ item.date + "&nbsp;" + item.time +"</p></div><div class=\"col-md-2 my-col dropdown\"><img src=\"https://i.postimg.cc/BQgBL3Fm/ellipsis.png\" class=\"menu-image dropdown-toggle\" id=\"dropdownMenuButton1\" data-bs-toggle=\"dropdown\" aria-expanded=\"false\"><ul class=\"dropdown-menu\" aria-labelledby=\"dropdownMenuButton1\"><li><a class=\"dropdown-item\" id=\"add-to-list-id\" onclick=\"unfriend('" + item.id + "')\">Unfriend</a></li></ul></div></div>"
                ));
                list_container.innerHTML = temp;
            }
            
        }
    });
}


function action_taken(id, action) {
    let csrfToken = $("input[name=csrfmiddlewaretoken").val();
    $.ajax({
        type: 'POST',
        url: '/account/accept-reject-request/',
        data: {
            'notification_id': id,
            'action': action,
            csrfmiddlewaretoken: csrfToken
        },
        dataType: 'json', 
        
        success: function (res) {
            console.log(res);
        }
    });
}


