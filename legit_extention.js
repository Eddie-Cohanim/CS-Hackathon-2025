// ==UserScript==
// @name         (softer colours)
// @namespace    http://localhost
// @version      0.21
// @description  colour each sentence: green ✅ / red ❌ / yellow ⚠
// @match        *://*/*
// @grant        GM_xmlhttpRequest
// @connect      127.0.0.1
// @run-at       document-end
// ==/UserScript==
(() => {
  "use strict";
  if (window.top !== window) return; // ignore iframes

  const API = "http://127.0.0.1:5000/verify_facts";

  /* ─────────────────────────────────── nicer-looking palette ──────── */
  const css = document.createElement("style");
  css.textContent = `
    /* apply to <mark>, <span>, or anything that gets the class */
    .fact-true  {                               /* ✅ confirmed fact   */
      background : rgba( 20,210, 0,.4);
      box-shadow : 0 0 0 2px rgba( 0,235, 0,.5) inset;
      border-radius:4px; padding:0 2px;
    }
    .fact-false {                               /* ❌ contradicted     */
      background : rgba(210, 20, 0,.4);
      box-shadow : 0 0 0 2px rgba(235, 0, 0,.5) inset;
      border-radius:4px; padding:0 2px;
    }
    .fact-skip  {                               /* ⚠ non-factual       */
      background : rgba(255,207, 72,.22);
      box-shadow : 0 0 0 2px rgba(255,207, 72,.28) inset;
      border-radius:4px; padding:0 2px;
    }
    .fact-await {                               /* ⏳ placeholder      */
      background : rgba(0,0,0,.10);
      box-shadow : 0 0 0 2px rgba(0,0,0,.14) inset;
      border-radius:4px; padding:0 2px;
    }
  `;
  document.head.appendChild(css);

  /* … everything below is unchanged … */

  /* ---------------------------------------------- sentence splitter */
  const splitter = (() => {
    const RX = /([.!?]|[:־])\s+|\n+/g; // also splits on Hebrew “:” / “־”
    return text => {
      const parts = text.split(RX).filter(Boolean);
      const out = [];
      for (let i = 0; i < parts.length; i += 2) {
        const chunk = (parts[i] || '') + (parts[i + 1] || '');
        if (chunk.trim()) out.push(chunk.trim());
      }
      return out;
    };
  })();

  /* --------------------------------------------- prepare paragraphs */
  function wrapSentences(pElem) {
    const raw = pElem.innerText;
    const sents = splitter(raw);
    if (sents.length === 0) return [];

    const frag = document.createDocumentFragment();
    const spans = sents.map((txt, idx) => {
      const sp = document.createElement("span");
      sp.textContent = txt + " ";
      sp.classList.add("fact-await");
      sp.dataset.idx = idx;
      frag.appendChild(sp);
      return sp;
    });
    pElem.textContent = "";
    pElem.appendChild(frag);
    return spans;
  }

  /* ---------------------------------------------------- main routine */
  function processParagraph(p) {
    const spans = wrapSentences(p);
    if (spans.length === 0) return;

    const sentences = spans.map(sp => sp.textContent.trim());

    GM_xmlhttpRequest({
      method : "POST",
      url    : API,
      headers: { "Content-Type": "application/json" },
      data   : JSON.stringify({ sentences }),
      onload : res => {
        if (res.status !== 200) return console.warn("fact-api", res.status);
        const { results } = JSON.parse(res.responseText);
        results.forEach((r, i) => {
          spans[i].classList.remove("fact-await");
          spans[i].classList.add("fact-" + r.label);
        });
      },
      onerror : e => console.error("fact-api error", e)
    });
  }

  /* ------------------------------------------- wait for real text  */
  const ready = new Promise(resolve => {
    const haveText = () =>
      [...document.querySelectorAll("p")].some(p => p.innerText.trim().length > 10);
    if (haveText()) return resolve();
    new MutationObserver((m, o) => haveText() && (o.disconnect(), resolve()))
      .observe(document.body, { childList: true, subtree: true });
  });

  /* --------------------------------------------------------- kick-off */
  ready.then(() => {
    console.log("🟢 fact-checker activated on", location.hostname);
    [...document.querySelectorAll("p")]
      .filter(p => p.innerText.trim().length > 10)
      .forEach(processParagraph);
  });
})();
