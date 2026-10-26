/* Navigation help only; guide search and reading also work without JavaScript. */
(() => {
  "use strict";
  const toc = document.querySelector("[data-guide-toc]");
  if (toc && window.matchMedia("(max-width: 900px)").matches) toc.open = false;
  document.addEventListener("keydown", (event) => {
    if (event.isComposing || event.repeat || event.defaultPrevented) return;
    const typing = event.target.closest && event.target.closest('input, textarea, select, [contenteditable="true"]');
    if (event.altKey && !event.ctrlKey && !event.metaKey && !typing && event.code === "KeyG") {
      event.preventDefault();
      window.location.assign("/studio/guides");
    }
  });
})();
