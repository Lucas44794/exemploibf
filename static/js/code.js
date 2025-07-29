document.addEventListener("DOMContentLoaded", function () {
  const modoNoturnoToggle = document.getElementById("modo-noturno");
  const body = document.body;

  // Verifica se o usuário já ativou o modo noturno antes e aplica o tema
  const temaSalvo = localStorage.getItem("modoNoturno") || "light";
  body.setAttribute("data-bs-theme", temaSalvo);

  // Atualiza o estado do checkbox
  if (modoNoturnoToggle) {
    modoNoturnoToggle.checked = temaSalvo === "dark";

    modoNoturnoToggle.addEventListener("change", function () {
      const novoTema = modoNoturnoToggle.checked ? "dark" : "light";
      body.setAttribute("data-bs-theme", novoTema);
      localStorage.setItem("modoNoturno", novoTema);
    });
  }
});