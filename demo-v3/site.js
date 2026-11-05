const b = document.querySelector(".burger"), m = document.getElementById("menu");
b?.addEventListener("click", () => b.setAttribute("aria-expanded", m.classList.toggle("open")));
document.getElementById("devis")?.addEventListener("submit", e => {
  e.preventDefault();
  document.getElementById("merci").hidden = false;
  e.target.reset();
});
