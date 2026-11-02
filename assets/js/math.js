// Kramdown protects TeX from Markdown by emitting math/tex script elements.
// Restore delimiters before MathJax loads so it can typeset those expressions.
document.querySelectorAll('.prose script[type^="math/tex"]').forEach((source) => {
  const display = source.type.includes('mode=display');
  const target = document.createElement(display ? 'div' : 'span');
  target.textContent = display
    ? `\\[${source.textContent}\\]`
    : `\\(${source.textContent}\\)`;
  source.replaceWith(target);
});

window.MathJax = {
  svg: { fontCache: 'global' }
};
