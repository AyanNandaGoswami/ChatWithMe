const x = document.getElementById("notificationAudio");
const y = document.getElementById("chatAudio");

function playNotificationAudio() {
  x.play();
}

function playChatAudio() {
  y.play();
}

const user = JSON.parse(document.getElementById('logged-in-user').textContent);
const chatSocket = new WebSocket('ws://' + 'localhost:8001' + '/notifications?user=' + user['uuid']);

chatSocket.onopen = function() {
  console.log('CONNECTED');
};

chatSocket.onmessage = function(e) {
  const data = JSON.parse(e.data);
  console.log("Received:", data);

  const notificationList = document.querySelector('#notification-container');
  const badge = document.getElementById('notification_badge');
  let badgeCount = 0;

  // If single notification
  if (data.id && data.message) {
    playNotificationAudio();

    const notifHTML = `
      <div class="notification">
        <p>${data.message}</p>
        ${data.type === "friend_request"
          ? `<button type="button" class="btn btn-primary btn-sm" onclick="action_taken('${data.id}', 'accepted')">Accept</button>
             <button type="button" class="btn btn-secondary btn-sm" onclick="action_taken('${data.id}', 'rejected')">Reject</button>`
          : ""}
      </div>
    `;

    notificationList.innerHTML = notifHTML + notificationList.innerHTML;

    badgeCount = data.is_read ? 0 : 1;
    badge.style.display = badgeCount > 0 ? "block" : "none";
    badge.innerText = badgeCount;
  }

  // If array of notifications
  else if (Array.isArray(data)) {
    notificationList.innerHTML = "";
    data.forEach(noti => {
      if (!noti.is_read) badgeCount += 1;
      const notifHTML = `
        <div class="notification">
          <p>${noti.message}</p>
          ${noti.type === "friend_request"
            ? `<button type="button" class="btn btn-primary btn-sm" onclick="action_taken('${noti.id}', 'accepted')">Accept</button>
               <button type="button" class="btn btn-secondary btn-sm" onclick="action_taken('${noti.id}', 'rejected')">Reject</button>`
            : ""}
        </div>
      `;
      notificationList.innerHTML += notifHTML;
    });

    badge.style.display = badgeCount > 0 ? "block" : "none";
    badge.innerText = badgeCount;
  }
};
