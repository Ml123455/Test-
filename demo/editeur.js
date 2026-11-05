// Mode édition : ouvrir la page avec ?edit (ex. botarmory.com/demo/?edit). Sans ?edit, ne fait rien.
// Texte : cliquer et taper. Photo : cliquer dessus pour la remplacer. « Enregistrer » télécharge la page modifiée.
if (new URLSearchParams(location.search).has("edit")) addEventListener("DOMContentLoaded", () => {
  document.designMode = "on";
  const ui = document.createElement("div");
  ui.id = "editeur-ui";
  ui.style.cssText = "position:fixed;bottom:16px;right:16px;z-index:99999;background:#1b1b1b;color:#fff;padding:12px 14px;border-radius:10px;font:14px/1.4 sans-serif;box-shadow:0 4px 20px #0006;max-width:260px";
  ui.innerHTML = '<b>Mode édition</b><br><small>Clique sur un texte pour le changer, sur une photo pour la remplacer.</small><br><button style="margin-top:8px;padding:8px 14px;border:0;border-radius:6px;background:#c9a24d;font-weight:700;cursor:pointer">Enregistrer la page</button>';
  document.body.append(ui);
  const pick = document.createElement("input");
  pick.type = "file"; pick.accept = "image/*";
  let cible;
  pick.onchange = () => {
    const f = pick.files[0]; if (!f) return;
    const img = new Image();
    img.onload = () => {
      const k = Math.min(1, 1400 / img.width), c = document.createElement("canvas");
      c.width = img.width * k; c.height = img.height * k;
      c.getContext("2d").drawImage(img, 0, 0, c.width, c.height);
      cible.src = c.toDataURL("image/jpeg", .85); cible.removeAttribute("srcset");
    };
    img.src = URL.createObjectURL(f); pick.value = "";
  };
  // capture : empêche les liens, boutons et fenêtres du site de se déclencher pendant l'édition
  document.addEventListener("click", e => {
    if (ui.contains(e.target)) return;
    e.preventDefault(); e.stopImmediatePropagation();
    const img = e.target.closest("img"); if (img) { cible = img; pick.click(); }
  }, true);
  ui.querySelector("button").onclick = () => {
    const copie = document.documentElement.cloneNode(true);
    copie.querySelector("#editeur-ui").remove();
    const a = document.createElement("a");
    a.href = URL.createObjectURL(new Blob(["<!doctype html>\n" + copie.outerHTML], { type: "text/html" }));
    a.download = "index-modifie.html"; a.click();
  };
});
