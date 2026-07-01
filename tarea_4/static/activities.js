const searchInput = document.getElementById('searchInput');
const resultsContainer = document.getElementById('resultsContainer');
let debounceTimer;

function escapeHtml(value) {
  return value
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

function highlightMatches(text, term) {
  if (!term || !text) {
    return escapeHtml(text || '');
  }

  const safeTerm = term.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const regex = new RegExp(safeTerm, 'gi');
  return escapeHtml(text).replace(regex, match => `<mark>${match}</mark>`);
}

function renderResult(activity, term) {
  const highlightedName = highlightMatches(activity.name, term);
  const highlightedDescription = highlightMatches(activity.description || '', term);
  const highlightedMunicipality = highlightMatches(activity.municipality, term);
  const highlightedMemberName = highlightMatches(activity.memberName, term);
  const highlightedType = highlightMatches(activity.type, term);
  const dayValue = activity.day || '';

  const gradeValue = activity.grade === '-' ? '-' : escapeHtml(activity.grade.toString());
  return `
    <article class="result-card">
      <h2>${highlightedName}</h2>
      <p><strong>Member:</strong> ${highlightedMemberName}</p>
      <p><strong>Day:</strong> ${escapeHtml(dayValue)}</p>
      <p><strong>Type:</strong> ${highlightedType}</p>
      <p><strong>Municipality:</strong> ${highlightedMunicipality}</p>
      <p><strong>Description:</strong> ${highlightedDescription || '<span class="empty">No description provided</span>'}</p>
      <p><strong>Grade:</strong> ${gradeValue}</p>
      <p><a href="/activities/${activity.id}" onclick="console.log('navigate to activity', ${activity.id})">Grade this activity</a></p>
    </article>
  `;
}

function renderEmpty(message) {
  resultsContainer.innerHTML = `<p class="status-message">${escapeHtml(message)}</p>`;
}

function clearResults() {
  resultsContainer.innerHTML = '';
}

function searchActivities(term) {
  const trimmed = term.trim();
  if (trimmed.length < 3) {
    clearResults();
    return;
  }

  fetch(`/api/activities/search?q=${encodeURIComponent(trimmed)}`)
    .then(response => response.json())
    .then(items => {
      if (!items || items.length === 0) {
        renderEmpty('No matching activities found.');
        return;
      }

      resultsContainer.innerHTML = items.map(item => renderResult(item, trimmed)).join('');
    })
    .catch(() => {
      renderEmpty('Unable to load search results. Please try again later.');
    });
}

searchInput.addEventListener('input', (event) => {
  clearTimeout(debounceTimer);
  debounceTimer = setTimeout(() => {
    searchActivities(event.target.value);
  }, 250);
});
