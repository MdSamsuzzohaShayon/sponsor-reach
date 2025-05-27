// Load and display CSV data
const CSV_PATH = 'csv/2025-04-26-new_sponsors.csv';
const MAX_ROWS = 10;
let allRows = [];
let currentRowIndex = 0;

function parseCSV(text) {
  const lines = text.trim().split('\n');
  const headers = lines[0].split(',');

  return lines.slice(1).map((line, index) => {
    const cols = line.split(',');
    return {
      id: index + 1,
      name: cols[0],
      city: cols[1],
      county: cols[2],
      typeRating: cols[3],
      route: cols[4],
      email: cols[5] || 'N/A'
    };
  });
}

function renderRows(rows) {
  const tbody = document.getElementById('sponsorBody');
  rows.forEach(row => {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td>${row.id}</td>
      <td>${row.name}</td>
      <td>${row.city}</td>
      <td>${row.county}</td>
      <td>${row.typeRating}</td>
      <td>${row.route}</td>
      <td>${row.email}</td>
    `;
    tbody.appendChild(tr);
  });
}

function loadMoreRows() {
  const nextRows = allRows.slice(currentRowIndex, currentRowIndex + MAX_ROWS);
  renderRows(nextRows);
  currentRowIndex += MAX_ROWS;
  if (currentRowIndex >= allRows.length) {
    document.getElementById('loadMoreBtn').style.display = 'none';
  }
}

window.onload = async () => {
  try {
    const response = await fetch(CSV_PATH);
    const text = await response.text();
    allRows = parseCSV(text);
    loadMoreRows(); // initial load

    document.getElementById('loadMoreBtn').addEventListener('click', loadMoreRows);
  } catch (err) {
    console.error('Failed to load CSV:', err);
  }
};
