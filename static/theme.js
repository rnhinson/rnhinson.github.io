// Light/dark switch. Follows the system setting until the reader picks one.
(function () {
  var root = document.documentElement;
  var button = document.getElementById("theme");
  var system = matchMedia("(prefers-color-scheme: dark)");

  function current() {
    return root.dataset.theme || (system.matches ? "dark" : "light");
  }
  function label() {
    var next = current() === "dark" ? "light" : "dark";
    button.textContent = next;
    button.setAttribute("aria-label", "Switch to " + next + " mode");
  }

  button.addEventListener("click", function () {
    var next = current() === "dark" ? "light" : "dark";
    root.dataset.theme = next;
    try { localStorage.setItem("theme", next); } catch (e) {}
    label();
  });
  system.addEventListener("change", label);

  label();
  button.hidden = false;
})();
