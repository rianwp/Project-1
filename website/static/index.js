function deleteData(databarangId) {
  fetch("/delete", {
    method: "POST",
    body: JSON.stringify({ databarangId: databarangId }),
  }).then((_res) => {
    window.location.href = "/barang";
  });
}

function changeText(barang) {
  const element = document.getElementById(barang);

  document.getElementById("test").innerHTML = element.innerHTML;
}

var totalHarga = 0;
var allTransaksi = [];

function ambilInput(nama, harga, jumlah, id, stock) {
  const jumlahtransaksi = document.getElementById(jumlah).value;

  if (jumlahtransaksi == "" || jumlahtransaksi == "0" || parseInt(stock) < parseInt(jumlahtransaksi)) {
    jumlahtransaksi = 0;
  } else {
    const table = document.getElementById("tabletransaksi");
    const row = table.insertRow(-1);
    const cell1 = row.insertCell(0);
    const cell2 = row.insertCell(1);
    const cell3 = row.insertCell(2);

    const transaksi = {
      id: id,
      jumlah: parseInt(jumlahtransaksi),
    };

    allTransaksi.push(transaksi);

    cell1.innerHTML = nama;
    cell2.innerHTML = "Rp." + harga;
    cell3.innerHTML = jumlahtransaksi;
    totalHarga = totalHarga + parseInt(harga) * parseInt(jumlahtransaksi);
    document.getElementById("totalharga").innerHTML = "Rp. " + totalHarga;
  }
}

function updateTransaksi() {
  const myJSONstring = JSON.stringify(allTransaksi);
  fetch("/updatetransaksi", {
    method: "POST",
    body: myJSONstring,
  }).then((_res) => {
    window.location.href = "/transaksi";
  });
}

function showChart(m1, m2, m3, m4, m5, m6, m7, m8, m9, m10, m11, m12, year) {
  const ctx = document.getElementById("myChart").getContext("2d");
  const myChart = new Chart(ctx, {
    type: "bar",
    data: {
      labels: ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"],
      datasets: [
        {
          label: "Kuantitas Penjualan Tahun " + year,
          data: [m1, m2, m3, m4, m5, m6, m7, m8, m9, m10, m11, m12],
          backgroundColor: ["rgba(255, 99, 132, 1)", "rgba(54, 162, 235, 1)", "rgba(255, 206, 86, 1)", "rgba(75, 192, 192, 1)", "rgba(153, 102, 255, 1)", "rgba(255, 159, 64, 1)"],
        },
      ],
    },
    options: {
      scales: {
        y: {
          beginAtZero: true,
        },
      },
    },
  });
}

document.getElementById("file").onchange = function () {
  document.getElementById("formimg").submit();
};
