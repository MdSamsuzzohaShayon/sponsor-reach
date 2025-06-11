const BASE_PATH = 'csv/';
const MAX_ROWS = 50;
let allRows = [];
let currentRowIndex = 0;

// Format Date to YYYY-MM-DD
function formatDate(date) {
  return date.toISOString().split('T')[0];
}

// Get dates for today and previous 5 days
function getRecentDates(days = 5) {
  const dates = [];
  for (let i = 0; i <= days; i++) {
    const d = new Date();
    d.setDate(d.getDate() - i);
    dates.push(formatDate(d));
  }
  return dates;
}

// Try to fetch the first available CSV file from the date list
async function findAvailableCSV() {
  const dates = getRecentDates();
  for (const date of dates) {
    const path = `${BASE_PATH}${date}-new_sponsors.csv`;
    try {
      const response = await fetch(path);
      if (response.ok) {
        console.log(`Loaded CSV from: ${path}`);
        return await response.text();
      }
    } catch (err) {
      // Ignore error, try next date
    }
  }
  throw new Error('No recent CSV file found.');
}

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
    const csvText = await findAvailableCSV();
    allRows = parseCSV(csvText);

    if (allRows.length === 0) {
      document.getElementById('sponsorTable').outerHTML = `<div class="alert alert-warning text-center" role="alert">
        No sponsor data available in the latest CSV file.
      </div>`;
      document.getElementById('loadMoreBtn').style.display = 'none';
      return;
    }

    loadMoreRows(); // initial load
    document.getElementById('loadMoreBtn').addEventListener('click', loadMoreRows);
  } catch (err) {
    console.error(err.message);
    document.getElementById('sponsorTable').outerHTML = `<div class="alert alert-danger text-center" role="alert">
      Sorry, no recent sponsor data is available.
    </div>`;
    document.getElementById('loadMoreBtn').style.display = 'none';
  }
};

