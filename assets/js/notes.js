(() => {
  const tools = document.querySelector('[data-note-tools]');
  if (!tools) return;
  const rows = [...document.querySelectorAll('[data-search]')];
  const search = document.querySelector('#note-search');
  const select = document.querySelector('#note-tag');
  const tags = [...new Set(rows.flatMap(row => row.dataset.tags.split('|').filter(Boolean)))].sort();
  tags.forEach(tag => select.add(new Option(tag, tag)));
  const requested = new URLSearchParams(location.search).get('tag');
  if (tags.includes(requested)) select.value = requested;
  function filter() {
    const query = search.value.toLowerCase().trim();
    let visible = 0;
    rows.forEach(row => {
      row.hidden = !row.dataset.search.toLowerCase().includes(query) || (select.value !== '' && !row.dataset.tags.split('|').includes(select.value));
      if (!row.hidden) visible++;
    });
    document.querySelector('#note-count').textContent = `${visible} ${visible === 1 ? 'note' : 'notes'}`;
    document.querySelector('[data-no-results]').hidden = visible !== 0;
    const url = new URL(location.href);
    if (select.value) url.searchParams.set('tag', select.value); else url.searchParams.delete('tag');
    history.replaceState(null, '', url);
  }
  tools.hidden = false;
  search.addEventListener('input', filter);
  select.addEventListener('change', filter);
  filter();
})();
