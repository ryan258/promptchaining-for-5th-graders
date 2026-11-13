(() => {
  "use strict";

  document.querySelectorAll("[data-lab-step]").forEach((step, index) => {
    const prompt = step.querySelector("[data-lab-prompt]");
    const inserts = step.querySelector("[data-lab-inserts]");
    const handoffs = step.querySelector("[data-lab-handoffs]");
    let visited = false;
    prompt.addEventListener("focus", () => { visited = true; });
    inserts.hidden = false;

    function showHandoffs() {
      if (!handoffs) return;
      const answers = [...new Set(Array.from(prompt.value.matchAll(/\[Answer\s+([0-9]+)\]/gi), match => Number(match[1])))];
      handoffs.textContent = answers.some(number => number < 1 || number > index)
        ? "Choose answers from earlier steps."
        : answers.length ? "Uses " + answers.map(number => "answer " + number).join(", ") + "." : "";
      handoffs.hidden = !handoffs.textContent;
    }
    prompt.addEventListener("input", showHandoffs);
    showHandoffs();

    inserts.addEventListener("click", (event) => {
      const button = event.target.closest("[data-lab-insert]");
      if (!button) return;

      const start = visited ? prompt.selectionStart : prompt.value.length;
      const end = visited ? prompt.selectionEnd : start;
      const before = prompt.value.slice(0, start);
      const after = prompt.value.slice(end);
      const prefix = before && !/\s$/.test(before) ? " " : "";
      const suffix = after && !/^\s/.test(after) ? " " : "";
      const insert = prefix + button.dataset.labInsert + suffix;
      if (before.length + insert.length + after.length > prompt.maxLength) {
        window.studioMessage("Shorten this prompt before adding another piece.");
        prompt.focus();
        return;
      }
      prompt.setRangeText(insert, start, end, "end");
      showHandoffs();
      prompt.focus();
    });
  });

  const reuse = document.querySelector("[data-lab-reuse]");
  if (reuse) {
    const answer = reuse.form.elements.namedItem("answer");
    const original = reuse.form.querySelector("[data-lab-previous-answer]");
    reuse.hidden = false;
    reuse.addEventListener("click", () => {
      answer.value = original.content.textContent;
      answer.focus();
    });
  }
})();
