document.addEventListener("DOMContentLoaded", function () {
  //   document.querySelector("#edit").addEventListener("click", () => edit());
  //   document
  //     .querySelector("#edit_submit")
  //     .addEventListener("click", () => submit());
  //   default
  // document.querySelectorAll("default_display").style.display = "block";
  // document.querySelectorAll("default_displaynone").style.display = "none";
  // document.querySelectorAll("default_display").style.display = "block";
  // document.querySelectorAll("default_displaynone").style.display = "none";
});

function submit(id) {
  console.log(`submit${id}`);
  const container = document.querySelector(`#post_edit_${id}`);
  const inputvalue = container.querySelector("textarea").value;
  // console.log(inputvalue);

  fetch(`/edit/${id}`, {
    // fetch 에 parameter 넣을려면 ` (1옆에 있는 특수문자) 사용해야 한다.
    method: "PUT",
    body: JSON.stringify({
      content: inputvalue,
    }),
  });

  // fetch(`/edit/${id}`)
  //   .then((response) => response.json())
  //   .then((post) => {
  //     console.log(post);
  //     document.querySelector(`#post_content_${id}`).innerHTML = "";
  //   });

  document.querySelector(
    `#post_content_${id}`
  ).innerHTML = `Content: ${inputvalue}`;
  document.querySelector(`#post_content_${id}`).style.display = "block";
  document.querySelector(`#post_edit_${id}`).style.display = "none";
  document.querySelector(`#edit_${id}`).style.display = "block";
  document.querySelector(`#edit_submit_${id}`).style.display = "none";

  container.querySelector("textarea").value = "";
}

function edit(id) {
  console.log(`edit_${id}`);

  // queryselectorAll은 list 주기 때문에 바로 style 적용 불가
  // 밑처럼 Foreach사용도 되고 forloop도 된다.
  Array.from(document.querySelectorAll(".default_display")).forEach(function (
    val
  ) {
    val.style.display = "block";
  });
  Array.from(document.querySelectorAll(".default_displaynone")).forEach(
    function (val) {
      val.style.display = "none";
    }
  );

  document.querySelector(`#post_content_${id}`).style.display = "none";
  document.querySelector(`#post_edit_${id}`).style.display = "block";
  document.querySelector(`#edit_${id}`).style.display = "none";
  document.querySelector(`#edit_submit_${id}`).style.display = "block";
}

// function like(id) {
//   const username = document
//     .querySelector(".nav-link")
//     .querySelector("strong").innerHTML;
//   console.log(username);
//   console.log(`like_${id}`);
//   fetch(`/edit/${id}`, {
//     // fetch 에 parameter 넣을려면 ` (1옆에 있는 특수문자) 사용해야 한다.
//     method: "PUT",
//     body: JSON.stringify({
//       liker: `User: a`,
//     }),
//   });
// }
