document.addEventListener("DOMContentLoaded", function () {
  // Use buttons to toggle between views
  document
    .querySelector("#inbox")
    .addEventListener("click", () => load_mailbox("inbox"));
  document
    .querySelector("#sent")
    .addEventListener("click", () => load_mailbox("sent"));
  document
    .querySelector("#archived")
    .addEventListener("click", () => load_mailbox("archive"));

  document.querySelector("#compose").addEventListener("click", compose_email);

  document
    .querySelector("#compose-form")
    .addEventListener("submit", send_email);

  // By default, load the inbox
  load_mailbox("inbox");
});

function compose_email() {
  // Show compose view and hide other views
  document.querySelector("#emails-view").style.display = "none";
  document.querySelector("#emails-view-items").style.display = "none";
  document.querySelector("#compose-view").style.display = "block";
  document.querySelector("#emails-view-item").style.display = "none";
  // Clear out composition fields
  document.querySelector("#compose-recipients").value = "";
  document.querySelector("#compose-subject").value = "";
  document.querySelector("#compose-body").value = "";
}

function add_email(contents) {
  const email = document.createElement("div");

  email.className = `email d-flex ${contents.id}`;
  email.innerHTML =
    `<div id="${contents.id}" onclick="view_email(this.id)" class="p-2">${contents.recipients}</div>` +
    `<div id="${contents.id}" onclick="view_email(this.id)" class="p-2">${contents.subject}</div>` +
    `<div class="ml-auto p-2">${contents.timestamp}</div>`;

  document.querySelector("#emails-view-items").append(email);
}

function add_email_inbox(contents) {
  const email = document.createElement("div");

  if (contents.read === false) {
    email.className = `email d-flex ${contents.id}`;
    email.innerHTML =
      `<div id="${contents.id}" onclick="view_email(this.id)" class="p-2">${contents.recipients}</div>` +
      `<div id="${contents.id}" onclick="view_email(this.id)" class="p-2">${contents.subject}</div>` +
      `<div class="ml-auto p-2 d-flex"><div class="p-2">${contents.timestamp}</div>` +
      `<button id="${contents.id}" onclick="archive_email(this.id)" class="ml-auto">archive</butt></div>`;
  } else {
    email.className = `email d-flex ${contents.id} backgroundgray`;
    email.innerHTML =
      `<div id="${contents.id}" onclick="view_email(this.id)" class="p-2">${contents.recipients}</div>` +
      `<div id="${contents.id}" onclick="view_email(this.id)" class="p-2">${contents.subject}</div>` +
      `<div class="ml-auto p-2 d-flex"><div class="p-2">${contents.timestamp}</div>` +
      `<button id="${contents.id}" onclick="archive_email(this.id)" class="ml-auto">archive</butt></div>`;
  }

  document.querySelector("#emails-view-items").append(email);
}
function add_email_archive(contents) {
  const email = document.createElement("div");

  if (contents.read === false) {
    email.className = `email d-flex ${contents.id}`;
    email.innerHTML =
      `<div id="${contents.id}" onclick="view_email(this.id)" class="p-2">${contents.recipients}</div>` +
      `<div id="${contents.id}" onclick="view_email(this.id)" class="p-2">${contents.subject}</div>` +
      `<div class="ml-auto p-2 d-flex"><div class="p-2">${contents.timestamp}</div>` +
      `<button id="${contents.id}" onclick="unarchive_email(this.id)" class="ml-auto">unarchive</butt></div>`;
  } else {
    email.className = `email d-flex ${contents.id} backgroundgray`;
    email.innerHTML =
      `<div id="${contents.id}" onclick="view_email(this.id)" class="p-2">${contents.recipients}</div>` +
      `<div id="${contents.id}" onclick="view_email(this.id)" class="p-2">${contents.subject}</div>` +
      `<div class="ml-auto p-2 d-flex"><div class="p-2">${contents.timestamp}</div>` +
      `<button id="${contents.id}" onclick="unarchive_email(this.id)" class="ml-auto">unarchive</butt></div>`;
  }
  document.querySelector("#emails-view-items").append(email);
}

function archive_email(id) {
  fetch(`/emails/${id}`, {
    // fetch 에 parameter 넣을려면 ` (1옆에 있는 특수문자) 사용해야 한다.
    method: "PUT",
    body: JSON.stringify({
      archived: true,
    }),
  }).then(() => load_mailbox("inbox"));
  // then ( () => function ) 이렇게 안하면 fetch기능 완료되기 전에 load_mailbox 되서 업데이트 되기전 메일 로드된다. 원리 정확히 모르겠다.
}
function unarchive_email(id) {
  fetch(`/emails/${id}`, {
    // fetch 에 parameter 넣을려면 ` (1옆에 있는 특수문자) 사용해야 한다.
    method: "PUT",
    body: JSON.stringify({
      archived: false,
    }),
  }).then(() => load_mailbox("inbox"));
  // alert(id);
}

function load_mailbox(mailbox) {
  // Show the mailbox and hide other views
  document.querySelector("#emails-view").style.display = "block";
  document.querySelector("#emails-view-items").style.display = "block";
  document.querySelector("#compose-view").style.display = "none";
  document.querySelector("#emails-view-item").style.display = "none";

  document.querySelector("#emails-view-items").innerHTML = "";
  // 이걸 안더해주면 mailbox 버튼 클릭할때마다 append되서 mail list 계속 늘어남

  // Show the mailbox name
  document.querySelector("#emails-view").innerHTML = `<h3>${
    mailbox.charAt(0).toUpperCase() + mailbox.slice(1)
  }</h3>`;

  fetch(`/emails/${mailbox}`)
    .then((response) => response.json())
    .then((emails) => {
      // Print emails
      console.log(emails);

      // ... do something else with emails ...

      if (`${mailbox}` === "inbox") {
        emails.forEach(add_email_inbox);
      }
      if (`${mailbox}` === "archive") {
        emails.forEach(add_email_archive);
      }
      if (`${mailbox}` === "sent") {
        emails.forEach(add_email);
      }
    });
}

function send_email(event) {
  event.preventDefault();
  // preventdefault() 사용 하면 default redirection (inbox) 막을 수 있다. 1시간 넘게걸림
  const recipients = document.querySelector("#compose-recipients").value;
  const subject = document.querySelector("#compose-subject").value;
  const body = document.querySelector("#compose-body").value;

  fetch("/emails", {
    method: "POST",
    body: JSON.stringify({
      recipients: recipients,
      subject: subject,
      body: body,
    }),
  })
    .then((response) => response.json())
    .then((result) => {
      console.log(result);
    })
    .then(() => load_mailbox("sent"));
}

function view_email(id) {
  document.querySelector("#emails-view").style.display = "none";
  document.querySelector("#emails-view-items").style.display = "none";
  document.querySelector("#emails-view-item").style.display = "block";
  document.querySelector("#compose-view").style.display = "none";

  document.querySelector("#emails-view-item").innerHTML = "";

  // read : True 로 변경
  fetch(`/emails/${id}`, {
    method: "PUT",
    body: JSON.stringify({
      read: true,
    }),
  });
  // document.querySelector("body").style.backgroundColor = "gray";

  fetch(`/emails/${id}`)
    .then((response) => response.json())
    .then((email) => {
      // Print emails
      console.log(email);
      // ... do something else with emails ...
      const sender = email.sender;
      const recipients = email.recipients;
      const subject = email.subject;
      const timestamp = email.timestamp;
      const body = email.body;

      const view = document.createElement("div");
      view.className = "view";
      view.innerHTML =
        `<div class="email_heading"><p>Sender: ${sender}</p>` +
        `<p>Recipients: ${recipients}</p>` +
        `<p>Subject: ${subject}</p>` +
        `<p>Timestamp: ${timestamp}</p>` +
        `<button value="${id} " class="reply" onclick="reply(this.value)">Reply</button></div>` +
        `<p class="email_body">${body}</p>`;

      document.querySelector("#emails-view-item").append(view);
    });
}

function reply(id) {
  fetch(`/emails/${id}`)
    .then((response) => response.json())
    .then((email) => {
      console.log(email.sender);

      // Show compose view and hide other views
      document.querySelector("#emails-view").style.display = "none";
      document.querySelector("#emails-view-items").style.display = "none";
      document.querySelector("#compose-view").style.display = "block";
      document.querySelector("#emails-view-item").style.display = "none";
      // Clear out composition fields
      document.querySelector("#compose-recipients").value = `${email.sender}`;
      document.querySelector("#compose-subject").value = `Re: ${email.subject}`;
      document.querySelector(
        "#compose-body"
      ).value = `On ${email.timestamp}, ${email.sender} wrote: "${email.body}"`;
    });
}
