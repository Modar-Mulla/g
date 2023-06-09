const postBtn = document.getElementById("post");

postBtn.addEventListener("click", (e) => {
  e.preventDefault();
  const modal = document.getElementById("modal");
  const backdrop = document.getElementById("backdrop");
  modal.style.opacity = "1";
  modal.style.display = "unset";
  backdrop.style.display = "block";

  let data = {
    "popultaionSZ": document.getElementById("popultaionSZ").value,
    "maxIter": document.getElementById("maxIter").value,
    "candidatesol": document.getElementById("candidatesol").value,
  }
  fetch("/calc", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  }
  ).then(response => {
    return response.json()
  }).then(json => {
    let ul = document.createElement("ul");
    ul.className = "list-group";
    let modalBody = document.getElementById("modal-body");
    modalBody.append(ul);
    json.map(li => {
      let newLi = document.createElement("li");
      newLi.textContent = li;
      newLi.className = "list-group-item";
      let ul = document.getElementsByClassName("list-group")[0];
      ul.append(newLi);
    })
  })

})


const closeModalBtn = document.getElementById("close");

closeModalBtn.addEventListener("click", () => {
  let ul = document.getElementsByClassName("list-group")[0];
  ul.remove();
  const modal = document.getElementById("modal");
  const backdrop = document.getElementById("backdrop");
  modal.style.opacity = "0";
  modal.style.display = "none";
  backdrop.style.display = "none";
})