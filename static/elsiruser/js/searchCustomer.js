const searchField = document.querySelector("#searchField");

const tableOutput = document.querySelector(".table-output");
const appTable = document.querySelector(".app-table");
const paginationContainer = document.querySelector(".pagination-container");
tableOutput.style.display = "none";
const noResults = document.querySelector(".no-results");
const tbody = document.querySelector(".table-body");


searchField.addEventListener("keyup", (e) => {
  const searchValue = e.target.value;
  noResults.style.display = "none";
 
  if (searchValue.trim().length > 0) {
    paginationContainer.style.display = "none";
    tbody.innerHTML = "";
    fetch('/search_customers/',{
      body: JSON.stringify({ searchText: searchValue }),
      method: "POST",
    })
      .then((res) => res.json())
      .then((data) => {
        console.log("data", data);
        appTable.style.display = "none";
        tableOutput.style.display = "block";

        console.log("data.length", data.length);

        if (data.length === 0) {
          noResults.style.display = "block";
          tableOutput.style.display = "none";
        } else {
          noResults.style.display = "none";
          data.forEach((item) => {
            tbody.innerHTML += `
                <tr>
                <td>${item.first_name}</td>
                <td>${item.second_name}</td>
                <td>${item.phone}</td>
                <td>${item.email_address}</td>
                <td>${item.debt}</td>
                <td>${item.loyalty_points}</td>
                <td><a class="btn btn-sm btn-primary" id="addpayment" href="/addSales/${item.id}">Pay</a></td>
                <td> <input type="button" value="Edit" class="btn btn-warning btn-sm btn-edit" data-sid="{{item.id}}"></td>
                </tr>`;
          });
        }
      });
  } else {
    tableOutput.style.display = "none";
    appTable.style.display = "block";
    paginationContainer.style.display = "block";
  }
});
