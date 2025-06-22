console.log("JS is working!");

const form = document.getElementById('treeForm');
const tableBody = document.querySelector('#treeTable tbody');

// Load existing trees when the page opens
window.onload = fetchTrees;

// Submit form
form.addEventListener('submit', function (e) {
  e.preventDefault();

  const data = {
    species: document.getElementById('treeName').value,
    planted_by: document.getElementById('planter').value,
    location: document.getElementById('location').value,
    date_planted: document.getElementById('datePlanted').value,
    status: document.getElementById('status').value
  };

  fetch('http://127.0.0.1:5000/tree', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  })
    .then(res => res.json())
    .then(response => {
      console.log("Tree added:", response);
      form.reset();
      fetchTrees(); // Refresh the table
    })
    .catch(err => console.error("Error adding tree:", err));
});

// Load all trees from backend
function fetchTrees() {
  console.log("Fetching trees...");
  fetch('http://127.0.0.1:5000/trees')
    .then(res => res.json())
    .then(data => {
      tableBody.innerHTML = '';

      data.forEach(tree => {
        const row = document.createElement('tr');
        row.innerHTML = `
          <td>${tree.species}</td>
          <td>${tree.planted_by}</td>
          <td>${tree.location}</td>
          <td>${tree.date_planted}</td>
          <td>${tree.status}</td>
          <td><button onclick="deleteTree(${tree.id})">🗑️</button></td>
        `;
        tableBody.appendChild(row);
      });
    })
    .catch(error => console.error("Error fetching trees:", error));
}

// Delete a tree
function deleteTree(id) {
  fetch(`http://127.0.0.1:5000/tree/${id}`, {
    method: 'DELETE'
  })
    .then(() => {
      console.log("Tree deleted:", id);
      fetchTrees(); // Refresh the table
    })
    .catch(err => console.error("Error deleting tree:", err));
}
